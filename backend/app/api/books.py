from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from app.db.database import query_db
from app.services.availability import availability_resolver

router = APIRouter()

@router.get("/books")
def list_books():
    rows = query_db(
        """SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.emotional_intensity, ba.setting, ba.themes 
        FROM books b 
        LEFT JOIN book_attributes ba ON b.id = ba.book_id 
        ORDER BY b.title ASC"""
    )
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "title": r["title"],
            "author": r["author"],
            "description": r["description"],
            "pages": r["pages"],
            "publication_year": r["publication_year"],
            "cover_url": r["cover_url"],
            "book_dna": {
                "mood": r["mood"] or "Balanced",
                "pacing": r["pacing"] or "Medium",
                "romance_level": r["romance_level"] or "Medium",
                "complexity": r["complexity"] or "Medium",
                "emotional_intensity": r["emotional_intensity"] or "Medium",
                "setting": r["setting"] or "General",
                "themes": r["themes"] or ""
            }
        })
    return {"books": results, "total": len(results)}

@router.get("/books/{book_id}")
def get_book_details(book_id: str):
    row = query_db(
        """SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.emotional_intensity, ba.setting, ba.themes 
        FROM books b 
        LEFT JOIN book_attributes ba ON b.id = ba.book_id 
        WHERE b.id = ?""",
        (book_id,),
        one=True
    )
    if not row:
        raise HTTPException(status_code=404, detail="Book not found.")
        
    avail = availability_resolver.get_availability(book_id)

    return {
        "id": row["id"],
        "title": row["title"],
        "author": row["author"],
        "description": row["description"],
        "pages": row["pages"],
        "publication_year": row["publication_year"],
        "cover_url": row["cover_url"],
        "book_dna": {
            "mood": row["mood"] or "Balanced",
            "pacing": row["pacing"] or "Medium",
            "romance_level": row["romance_level"] or "Medium",
            "complexity": row["complexity"] or "Medium",
            "emotional_intensity": row["emotional_intensity"] or "Medium",
            "setting": row["setting"] or "General",
            "themes": row["themes"] or ""
        },
        "availability": avail
    }

@router.get("/books/{book_id}/availability")
def get_book_availability_endpoint(book_id: str):
    book = query_db("SELECT id FROM books WHERE id = ?", (book_id,), one=True)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    avail = availability_resolver.get_availability(book_id)
    return {"book_id": book_id, "availability": avail}
