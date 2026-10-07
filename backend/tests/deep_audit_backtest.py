import json
import time
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db, ensure_default_user, query_db, execute_db
from app.ingestion.open_library import seed_books_to_db
from app.services.ai_provider import ai_provider
from app.services.ranker import ranker
from app.services.embeddings import generate_embedding, calculate_cosine_similarity
from app.services.comparison import comparator
from app.services.reading_path import reading_path_generator
from app.services.evaluation import evaluator

def run_deep_audit():
    print("=" * 75)
    print("      LITLENS DEEP FUNCTIONALITY AUDIT & BACKTESTING SUITE")
    print("=" * 75)

    # Step 1: Database Integrity & Schema Audit
    print("\n[AUDIT 1] Database Architecture & Schema Integrity...")
    init_db()
    ensure_default_user()
    seed_books_to_db()

    books = query_db("SELECT COUNT(*) as cnt FROM books", one=True)
    attributes = query_db("SELECT COUNT(*) as cnt FROM book_attributes", one=True)
    authors = query_db("SELECT COUNT(*) as cnt FROM authors", one=True)
    genres = query_db("SELECT COUNT(*) as cnt FROM genres", one=True)

    print(f"  Indexed Books Count: {books['cnt']}")
    print(f"  Book DNA Attributes Count: {attributes['cnt']}")
    print(f"  Authors Registry Count: {authors['cnt']}")
    print(f"  Genres Registry Count: {genres['cnt']}")
    assert books['cnt'] > 0 and attributes['cnt'] == books['cnt']
    print("  -> RESULT: Database Schema Integrity PASSED")

    client = TestClient(app)

    # Step 2: NLU Preference Extraction Backtesting
    print("\n[AUDIT 2] Natural Language Understanding (NLU) Backtesting...")
    test_queries = [
        {
            "query": "I want a dark mystery under 300 pages with a huge plot twist and almost no romance",
            "expected_genre": "Mystery",
            "expected_mood": "Dark",
            "max_pages": 300,
            "expected_romance": "Low"
        },
        {
            "query": "Give me a cozy comforting fantasy story with magical world and found family",
            "expected_genre": "Fantasy",
            "expected_mood": "Comforting",
            "max_pages": None,
            "expected_romance": "Any"
        },
        {
            "query": "Fast-paced sci-fi space exploration story without romance under 500 pages",
            "expected_genre": "Sci-Fi",
            "expected_pacing": "Fast",
            "max_pages": 500,
            "expected_romance": "Low"
        }
    ]

    for idx, tq in enumerate(test_queries, 1):
        extracted = ai_provider.extract_preferences(tq["query"])
        print(f"  Test Case 2.{idx}: '{tq['query']}'")
        print(f"    Extracted: {extracted}")
        if tq["expected_genre"] != "Any":
            assert extracted["genre"] in [tq["expected_genre"], "Any"]
        if "expected_mood" in tq and tq["expected_mood"] != "Any":
            assert extracted["mood"] in [tq["expected_mood"], "Any", "Suspenseful"]
        if tq.get("max_pages"):
            assert extracted["max_pages"] is not None and extracted["max_pages"] <= tq["max_pages"] + 50
    print("  -> RESULT: NLU Preference Extraction Backtesting PASSED")

    # Step 3: Hybrid Ranking Model Mathematical Audit
    print("\n[AUDIT 3] Hybrid Ranking Model Mathematical Verification...")
    nl_query = "I want a short dark mystery under 300 pages with high suspense and almost no romance."
    extracted = ai_provider.extract_preferences(nl_query)
    q_vec = generate_embedding(nl_query)

    sample_book = query_db(
        """SELECT b.*, ba.mood, ba.pacing, ba.romance_level, ba.complexity, ba.themes 
        FROM books b LEFT JOIN book_attributes ba ON b.id = ba.book_id LIMIT 1""",
        one=True
    )
    b_dict = dict(sample_book)
    score_res = ranker.score_book(b_dict, extracted, q_vec)

    sb = score_res["score_breakdown"]
    expected_score = float(max(0.05, min(0.99, (0.35 * sb["semantic_similarity"]) + (0.25 * sb["constraint_satisfaction"]) + (0.40 * sb["book_dna_match"]) - sb["history_penalty"])))
    
    print(f"  Scored Book: '{b_dict['title']}'")
    print(f"  Breakdown: Semantic={sb['semantic_similarity']}, Constraint={sb['constraint_satisfaction']}, DNA={sb['book_dna_match']}, History Penalty={sb['history_penalty']}")
    print(f"  Calculated Match Score: {score_res['match_score']} (Expected: {round(expected_score, 2)})")
    assert abs(score_res["match_score"] - round(expected_score, 2)) <= 0.02
    print("  -> RESULT: Ranking Score Model Mathematical Verification PASSED")

    # Step 4: "Change One Thing" Conversational Session State Backtest
    print("\n[AUDIT 4] 'Change One Thing' Conversational Session State...")
    disc_res = client.post("/api/discover", json={"query": "I want a sci-fi space novel"})
    assert disc_res.status_code == 200
    disc_data = disc_res.json()
    session_id = disc_data["session_id"]
    orig_prefs = disc_data["extracted_preferences"]

    ref1 = client.post("/api/refine", json={"session_id": session_id, "instruction": "Make it darker"})
    assert ref1.status_code == 200
    ref1_prefs = ref1.json()["updated_preferences"]
    print(f"  Refinement 1 ('Make it darker'): Mood changed from '{orig_prefs.get('mood')}' -> '{ref1_prefs['mood']}'")
    assert ref1_prefs["mood"] == "Dark"

    ref2 = client.post("/api/refine", json={"session_id": session_id, "instruction": "Shorter under 300 pages"})
    assert ref2.status_code == 200
    ref2_prefs = ref2.json()["updated_preferences"]
    print(f"  Refinement 2 ('Shorter'): Max Pages set to '{ref2_prefs['max_pages']}' (Mood preserved as '{ref2_prefs['mood']}')")
    assert ref2_prefs["mood"] == "Dark"
    assert ref2_prefs["max_pages"] is not None and ref2_prefs["max_pages"] <= 350
    print("  -> RESULT: Conversational State Preservation PASSED")

    # Step 5: Side-by-Side Preference-Aware Comparison Audit
    print("\n[AUDIT 5] Preference-Aware Side-by-Side Comparison Audit...")
    top_two = [b["id"] for b in disc_data["recommendations"][:2]]
    comp_res = client.post("/api/compare", json={"book_ids": top_two, "active_intent": ref2_prefs})
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    print(f"  Compared Books: {[b['title'] for b in comp_data['compared_books']]}")
    print(f"  Verdict: '{comp_data['verdict']}'")
    assert len(comp_data["compared_books"]) == 2
    assert "verdict" in comp_data
    print("  -> RESULT: Side-by-Side Comparison Audit PASSED")

    # Step 6: Reading History Penalty Signals Audit
    print("\n[AUDIT 6] Personal Reading History Penalty Signals...")
    test_user = "audit_user_1"
    target_book_id = disc_data["recommendations"][0]["id"]
    
    # Reject book
    client.post(f"/api/books/{target_book_id}/status", json={"user_id": test_user, "book_id": target_book_id, "status": "rejected"})
    
    # Discover again for same user
    new_disc = client.post("/api/discover", json={"query": "I want a sci-fi space novel", "user_id": test_user})
    new_recs = new_disc.json()["recommendations"]
    
    rejected_book_rec = next((b for b in new_recs if b["id"] == target_book_id), None)
    if rejected_book_rec:
        print(f"  Rejected Book Match Score after Penalty: {rejected_book_rec['match_score']} (History Penalty: {rejected_book_rec['score_breakdown']['history_penalty']})")
        assert rejected_book_rec["score_breakdown"]["history_penalty"] > 0
    else:
        print("  Rejected book fell completely out of top recommendations list.")
    print("  -> RESULT: Personal Reading History Rejection Signals PASSED")

    # Step 7: Progressive Reading Paths Audit
    print("\n[AUDIT 7] Progressive Reading Paths Audit...")
    path_res = client.post("/api/reading-path", json={"topic_or_genre": "Fantasy"})
    assert path_res.status_code == 200
    path_data = path_res.json()
    print(f"  Path Name: '{path_data['path_name']}' with {path_data['total_steps']} steps")
    for s in path_data["steps"]:
        print(f"    Stage {s['step']}: '{s['title']}' ({s['complexity']} complexity, {s['pages']} pages)")
    assert len(path_data["steps"]) >= 2
    print("  -> RESULT: Progressive Reading Paths Audit PASSED")

    # Step 8: Recommendation Evaluation Suite & Benchmark Experiment
    print("\n[AUDIT 8] Recommendation Evaluation Benchmark Experiment...")
    exp = evaluator.run_conventional_vs_nl_experiment()
    print(f"  Test Query: '{exp['test_query']}'")
    print(f"  Conventional Search Precision@5: {exp['conventional_search']['precision_at_5']}")
    print(f"  LitLens NL Search Precision@5:  {exp['natural_language_search']['precision_at_5']}")
    print(f"  Findings: {exp['findings']}")
    assert exp['natural_language_search']['precision_at_5'] >= exp['conventional_search']['precision_at_5']
    print("  -> RESULT: Recommendation Evaluation Benchmark PASSED")

    print("\n" + "=" * 75)
    print("      DEEP AUDIT & FUNCTIONALITY BACKTEST COMPLETE: 100% SUCCESS RATE")
    print("=" * 75)

if __name__ == "__main__":
    run_deep_audit()
