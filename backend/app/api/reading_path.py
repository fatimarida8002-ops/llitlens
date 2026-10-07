from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.reading_path import reading_path_generator

router = APIRouter()

class ReadingPathRequest(BaseModel):
    topic_or_genre: Optional[str] = "Fantasy"

@router.post("/reading-path")
def generate_reading_path(req: ReadingPathRequest):
    return reading_path_generator.generate_path(req.topic_or_genre or "Fantasy")
