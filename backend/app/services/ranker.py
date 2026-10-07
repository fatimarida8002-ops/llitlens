import json
from typing import Dict, Any, List, Tuple
from app.services.embeddings import generate_embedding, calculate_cosine_similarity

class HybridRanker:
    """
    Transparent ranking engine combining semantic vector similarity,
    hard/soft metadata constraints, Book DNA profile attributes, and user history signals.
    """
    
    def score_book(
        self,
        book: Dict[str, Any],
        extracted_prefs: Dict[str, Any],
        user_query_vec: List[float],
        user_history_rejected_ids: List[str] = None
    ) -> Dict[str, Any]:
        user_history_rejected_ids = user_history_rejected_ids or []
        
        # 1. Semantic Similarity Signal (Weight: 0.35)
        book_vec_raw = book.get("vector_json")
        if book_vec_raw:
            try:
                book_vec = json.loads(book_vec_raw)
            except Exception:
                book_vec = generate_embedding(f"{book['title']} {book['description']} {book.get('themes', '')}")
        else:
            book_vec = generate_embedding(f"{book['title']} {book['description']} {book.get('themes', '')}")
            
        semantic_sim = max(0.0, calculate_cosine_similarity(user_query_vec, book_vec))
        
        # 2. Hard Explicit Constraint Score (Weight: 0.25)
        constraint_score = 1.0
        
        # Page count constraint
        max_pages = extracted_prefs.get("max_pages")
        book_pages = book.get("pages", 300)
        if max_pages:
            if book_pages <= max_pages:
                constraint_score += 0.2
            else:
                over_percentage = (book_pages - max_pages) / max_pages
                constraint_score -= min(0.6, over_percentage * 0.5)

        # Explicit negative constraint penalties (e.g. "not horror", "no romance")
        for constraint in extracted_prefs.get("explicit_constraints", []):
            clow = constraint.lower()
            if "no romance" in clow or "without romance" in clow or "little romance" in clow:
                if book.get("romance_level") in ["High", "Medium"]:
                    constraint_score -= 0.4
            if "not horror" in clow or "no horror" in clow:
                if "horror" in book.get("genre", "").lower() or "horror" in book.get("subgenre", "").lower():
                    constraint_score -= 0.8
                    
        constraint_score = max(0.0, min(1.0, constraint_score))
        
        # 3. Book DNA Attribute Compatibility Score (Weight: 0.40)
        dna_score = 0.5
        dna_matches = []
        
        # Genre match
        req_genre = extracted_prefs.get("genre", "Any")
        if req_genre != "Any":
            if req_genre.lower() == book.get("genre", "").lower():
                dna_score += 0.2
                dna_matches.append(f"Genre: {req_genre}")
            else:
                dna_score -= 0.15

        # Mood match
        req_mood = extracted_prefs.get("mood", "Any")
        if req_mood != "Any":
            if req_mood.lower() in book.get("mood", "").lower():
                dna_score += 0.25
                dna_matches.append(f"Mood: {req_mood}")
            else:
                dna_score -= 0.1

        # Pacing match
        req_pacing = extracted_prefs.get("pacing", "Any")
        if req_pacing != "Any":
            if req_pacing.lower() == book.get("pacing", "").lower():
                dna_score += 0.15
                dna_matches.append(f"Pacing: {req_pacing}")

        # Romance level match
        req_romance = extracted_prefs.get("romance_level", "Any")
        if req_romance != "Any":
            if req_romance.lower() == book.get("romance_level", "").lower():
                dna_score += 0.15
                dna_matches.append(f"Romance: {req_romance}")
            elif req_romance == "Low" and book.get("romance_level") == "High":
                dna_score -= 0.35

        # Complexity match
        req_complexity = extracted_prefs.get("complexity", "Any")
        if req_complexity != "Any":
            if req_complexity.lower() == book.get("complexity", "").lower():
                dna_score += 0.15
                dna_matches.append(f"Complexity: {req_complexity}")

        dna_score = max(0.0, min(1.0, dna_score))
        
        # 4. User Reading History Penalty
        history_penalty = 0.0
        if book.get("id") in user_history_rejected_ids:
            history_penalty = 0.5 # Substantial penalty for user-rejected books

        # Weighted Final Score Calculation
        final_score = (
            (0.35 * semantic_sim) +
            (0.25 * constraint_score) +
            (0.40 * dna_score)
        ) - history_penalty
        
        final_score = float(max(0.05, min(0.99, final_score)))

        return {
            "book_id": book["id"],
            "match_score": round(final_score, 2),
            "score_breakdown": {
                "semantic_similarity": round(semantic_sim, 2),
                "constraint_satisfaction": round(constraint_score, 2),
                "book_dna_match": round(dna_score, 2),
                "history_penalty": round(history_penalty, 2)
            },
            "key_matches": dna_matches
        }

ranker = HybridRanker()
