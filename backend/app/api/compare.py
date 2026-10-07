from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.comparison import comparator

router = APIRouter()

class CompareRequest(BaseModel):
    book_ids: List[str]
    active_intent: Dict[str, Any]

@router.post("/compare")
def compare_books(req: CompareRequest):
    if not req.book_ids or len(req.book_ids) < 2:
        raise HTTPException(status_code=400, detail="Please select at least 2 books to compare.")
    return comparator.compare_books(req.book_ids, req.active_intent)
