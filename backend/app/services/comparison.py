import json
from typing import List, Dict, Any
from app.db.database import query_db

class BookComparator:
    """
    Evaluates and compares multiple candidate books side-by-side
    directly against the user's specific natural language reading intent.
    """
    
    def compare_books(self, book_ids: List[str], active_intent: Dict[str, Any]) -> Dict[str, Any]:
        if not book_ids:
            return {"error": "No book IDs provided for comparison."}
            
        placeholders = ",".join(["?"] * len(book_ids))
        rows = query_db(
            f"""SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.emotional_intensity, ba.setting, ba.themes 
            FROM books b 
            LEFT JOIN book_attributes ba ON b.id = ba.book_id 
            WHERE b.id IN ({placeholders})""",
            tuple(book_ids)
        )
        
        books_data = []
        for r in rows:
            books_data.append({
                "id": r["id"],
                "title": r["title"],
                "author": r["author"],
                "pages": r["pages"],
                "publication_year": r["publication_year"],
                "cover_url": r["cover_url"],
                "genre": r["description"] and "Mystery" if "mystery" in r["description"].lower() else "General",
                "mood": r["mood"] or "Medium",
                "pacing": r["pacing"] or "Medium",
                "romance_level": r["romance_level"] or "Medium",
                "complexity": r["complexity"] or "Medium",
                "setting": r["setting"] or "General",
                "themes": r["themes"] or ""
            })
            
        # Determine best match for current intent
        req_genre = active_intent.get("genre", "Any")
        req_mood = active_intent.get("mood", "Any")
        req_romance = active_intent.get("romance_level", "Any")
        max_pages = active_intent.get("max_pages")
        
        analysis = []
        best_fit = None
        best_score = -1
        
        for b in books_data:
            score = 0
            reasons = []
            
            if req_genre != "Any" and req_genre.lower() in b["genre"].lower():
                score += 3
                reasons.append(f"Matches requested genre '{req_genre}'")
                
            if req_mood != "Any" and req_mood.lower() in b["mood"].lower():
                score += 3
                reasons.append(f"Matches requested mood '{req_mood}'")
                
            if req_romance != "Any" and req_romance.lower() == b["romance_level"].lower():
                score += 2
                reasons.append(f"Matches requested romance level '{req_romance}'")
                
            if max_pages and b["pages"] <= max_pages:
                score += 2
                reasons.append(f"Satisfies length limit ({b['pages']} <= {max_pages} pages)")
                
            analysis.append({
                "book_id": b["id"],
                "title": b["title"],
                "intent_alignment_score": score,
                "strengths": reasons
            })
            
            if score > best_score:
                best_score = score
                best_fit = b["title"]
                
        summary_verdict = (
            f"Based on your request for a {req_mood} {req_genre} book, "
            f"'{best_fit}' aligns most strongly with your specified criteria."
        ) if best_fit else "Both books offer distinct reading experiences."

        return {
            "active_intent": active_intent,
            "compared_books": books_data,
            "analysis": analysis,
            "verdict": summary_verdict
        }

comparator = BookComparator()
