from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.db.database import query_db
from app.services.conversation import conversation_manager
from app.services.embeddings import generate_embedding
from app.services.ranker import ranker
from app.services.ai_provider import ai_provider
from app.services.availability import availability_resolver

router = APIRouter()

class RefineRequest(BaseModel):
    session_id: str
    instruction: str # e.g. "Make it darker", "Shorter", "Less romance"

@router.post("/refine")
def refine_recommendations(req: RefineRequest):
    session = conversation_manager.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Recommendation session not found.")
        
    # Apply single dimension refinement ("Change One Thing")
    updated_prefs = conversation_manager.apply_change_one_thing(req.session_id, req.instruction)
    
    # Re-score books based on modified preference state
    query_text = f"{session['original_query']} {req.instruction}"
    query_vec = generate_embedding(query_text)
    
    rows = query_db(
        """SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.emotional_intensity, ba.setting, ba.themes 
        FROM books b 
        LEFT JOIN book_attributes ba ON b.id = ba.book_id"""
    )
    
    scored_books = []
    for r in rows:
        b_dict = dict(r)
        score_res = ranker.score_book(b_dict, updated_prefs, query_vec)
        
        explanation = ai_provider.generate_spoiler_free_explanation(
            b_dict["title"], b_dict["author"], b_dict.get("description", ""), query_text, score_res["match_score"]
        )
        
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
            "book_dna": {
                "mood": b_dict.get("mood", "Balanced"),
                "pacing": b_dict.get("pacing", "Medium"),
                "romance_level": b_dict.get("romance_level", "Medium"),
                "complexity": b_dict.get("complexity", "Medium"),
                "emotional_intensity": b_dict.get("emotional_intensity", "Medium"),
                "setting": b_dict.get("setting", "General"),
                "themes": b_dict.get("themes", "")
            },
            "availability": avail
        })
        
    scored_books.sort(key=lambda x: x["match_score"], reverse=True)
    
    return {
        "session_id": req.session_id,
        "applied_instruction": req.instruction,
        "updated_preferences": updated_prefs,
        "recommendations": scored_books[:6]
    }
