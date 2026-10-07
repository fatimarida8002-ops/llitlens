from typing import List, Dict, Any
from app.db.database import query_db

class ReadingPathGenerator:
    """
    Generates progressive reading paths ordering books by complexity, length,
    and narrative depth for a guided reading journey.
    """
    
    def generate_path(self, genre_or_theme: str = "Fantasy") -> Dict[str, Any]:
        rows = query_db(
            """SELECT b.*, ba.complexity, ba.pacing, ba.mood, ba.romance_level, ba.themes 
            FROM books b 
            LEFT JOIN book_attributes ba ON b.id = ba.book_id 
            ORDER BY b.pages ASC"""
        )
        
        books = [dict(r) for r in rows]
        
        # Sort into progressive tiers: Entry -> Intermediate -> Advanced / Epic
        entry_tier = [b for b in books if (b.get("complexity") == "Easy" or b.get("pages", 300) < 350)]
        inter_tier = [b for b in books if (b.get("complexity") == "Medium" and 300 <= b.get("pages", 300) <= 500)]
        epic_tier = [b for b in books if (b.get("complexity") == "High" or b.get("pages", 300) > 500)]
        
        steps = []
        if entry_tier:
            b = entry_tier[0]
            steps.append({
                "step": 1,
                "stage": "Entry / Introduction",
                "book_id": b["id"],
                "title": b["title"],
                "author": b["author"],
                "pages": b["pages"],
                "complexity": b.get("complexity", "Easy"),
                "reason": "Accessible entry point with fast pacing and manageable length."
            })
            
        if inter_tier:
            b = inter_tier[0]
            steps.append({
                "step": 2,
                "stage": "Intermediate Exploration",
                "book_id": b["id"],
                "title": b["title"],
                "author": b["author"],
                "pages": b["pages"],
                "complexity": b.get("complexity", "Medium"),
                "reason": "Expands on world-building, themes, and emotional depth."
            })
            
        if epic_tier:
            b = epic_tier[0]
            steps.append({
                "step": 3,
                "stage": "Mastery / Epic Journey",
                "book_id": b["id"],
                "title": b["title"],
                "author": b["author"],
                "pages": b["pages"],
                "complexity": b.get("complexity", "High"),
                "reason": "Rich, multi-layered narrative demanding deeper reader engagement."
            })
            
        return {
            "path_name": f"Progressive {genre_or_theme} Journey",
            "total_steps": len(steps),
            "steps": steps
        }

reading_path_generator = ReadingPathGenerator()
