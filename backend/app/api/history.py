import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.db.database import query_db, execute_db

router = APIRouter()

class UserBookStatusRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    book_id: str
    status: str # 'saved', 'reading', 'read', 'rejected'
    rating: Optional[int] = None

@router.get("/history")
def get_user_history(user_id: str = "default_user"):
    rows = query_db(
        """SELECT ub.*, b.title, b.author, b.cover_url, b.pages 
        FROM user_books ub 
        JOIN books b ON ub.book_id = b.id 
        WHERE ub.user_id = ? 
        ORDER BY ub.updated_at DESC""",
        (user_id,)
    )
    return {"history": [dict(r) for r in rows]}

@router.post("/books/{book_id}/status")
def update_book_status(book_id: str, req: UserBookStatusRequest):
    if req.status not in ['saved', 'reading', 'read', 'rejected']:
        raise HTTPException(status_code=400, detail="Invalid status. Must be saved, reading, read, or rejected.")
        
    rec_id = f"ub_{uuid.uuid4().hex[:12]}"
    execute_db(
        """INSERT INTO user_books (id, user_id, book_id, status, rating) 
        VALUES (?, ?, ?, ?, ?) 
        ON CONFLICT(user_id, book_id) DO UPDATE SET 
        status = excluded.status, rating = excluded.rating, updated_at = CURRENT_TIMESTAMP""",
        (rec_id, req.user_id, book_id, req.status, req.rating)
    )
    return {"message": f"Book status updated to {req.status}.", "book_id": book_id, "status": req.status}
