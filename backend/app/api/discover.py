import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.db.database import query_db, execute_db
from app.services.ai_provider import ai_provider
from app.services.embeddings import generate_embedding
from app.services.ranker import ranker
from app.services.conversation import conversation_manager
from app.services.availability import availability_resolver

router = APIRouter()

class DiscoverRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"

class BookRecommendationResponse(BaseModel):
    id: str
    title: str
    author: str
    description: Optional[str]
    pages: int
    publication_year: Optional[int]
    cover_url: Optional[str]
    match_score: float
    explanation: str
    score_breakdown: Dict[str, float]
    book_dna: Dict[str, Any]
    availability: Optional[List[Dict[str, Any]]] = []

class DiscoverResponse(BaseModel):
    session_id: str
    original_query: str
    extracted_preferences: Dict[str, Any]
    recommendations: List[BookRecommendationResponse]

@router.post("/discover", response_model=DiscoverResponse)
def discover_books(req: DiscoverRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
        
    # 1. Natural Language Preference Extraction
    extracted = ai_provider.extract_preferences(req.query)
    
    # 2. Create Recommendation Session
    session_id = conversation_manager.create_session(req.user_id, req.query, extracted)
    
    # 3. Fetch user history (rejected books)
    rejected_rows = query_db(
        "SELECT book_id FROM user_books WHERE user_id = ? AND status = 'rejected'",
        (req.user_id,)
    )
    rejected_ids = [r["book_id"] for r in rejected_rows] if rejected_rows else []
    
    # 4. Generate query embedding vector
    query_vec = generate_embedding(req.query)
    
    # 5. Fetch all books & attributes from database
    rows = query_db(
        """SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.emotional_intensity, ba.setting, ba.themes, ba.attributes_json 
        FROM books b 
        LEFT JOIN book_attributes ba ON b.id = ba.book_id"""
    )
    
    if not rows:
        raise HTTPException(status_code=404, detail="No books currently available in corpus. Please run ingestion.")
        
    # 6. Candidate Ranking & Scoring
    scored_books = []
    for r in rows:
        b_dict = dict(r)
        score_res = ranker.score_book(b_dict, extracted, query_vec, rejected_ids)
        
        # Spoiler-free explanation
        explanation = ai_provider.generate_spoiler_free_explanation(
            b_dict["title"], b_dict["author"], b_dict.get("description", ""), req.query, score_res["match_score"]
        )
        
        dna = {
            "mood": b_dict.get("mood", "Balanced"),
            "pacing": b_dict.get("pacing", "Medium"),
            "romance_level": b_dict.get("romance_level", "Medium"),
            "complexity": b_dict.get("complexity", "Medium"),
            "emotional_intensity": b_dict.get("emotional_intensity", "Medium"),
            "setting": b_dict.get("setting", "General"),
            "themes": b_dict.get("themes", "")
        }
        
        # Fetch verified availability links for candidate book
        avail = availability_resolver.get_availability(b_dict["id"])

        scored_books.append({
            "id": b_dict["id"],
            "title": b_dict["title"],
            "author": b_dict["author"],
            "description": b_dict["description"],
            "pages": b_dict["pages"],
            "publication_year": b_dict["publication_year"],
            "cover_url": b_dict["cover_url"],
            "match_score": score_res["match_score"],
            "explanation": explanation,
            "score_breakdown": score_res["score_breakdown"],
            "book_dna": dna,
            "availability": avail
        })
        
    # Sort by transparent match score descending
    scored_books.sort(key=lambda x: x["match_score"], reverse=True)
    top_recommendations = scored_books[:6]
    
    # Store recommendations in database
    for idx, rec in enumerate(top_recommendations):
        execute_db(
            """INSERT INTO recommendations 
            (id, session_id, book_id, match_score, rank, explanation) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (f"rec_{idx}_{session_id}", session_id, rec["id"], rec["match_score"], idx + 1, rec["explanation"])
        )

    return {
        "session_id": session_id,
        "original_query": req.query,
        "extracted_preferences": extracted,
        "recommendations": top_recommendations
    }
