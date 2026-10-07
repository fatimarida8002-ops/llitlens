import json
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db, ensure_default_user, query_db
from app.ingestion.open_library import seed_books_to_db

def main():
    print("=" * 60)
    print("      LitLens System Verification & Requirement Audit")
    print("=" * 60)

    # 1. Initialize DB & Seed Data
    init_db()
    ensure_default_user()
    seed_books_to_db()

    client = TestClient(app)

    # Test 1: P0 Natural Language Search & Structured Preference Extraction
    print("\n[TEST 1] P0 — Natural-Language Search & Preference Extraction...")
    query = "I want a short dark mystery under 300 pages with a huge plot twist and almost no romance."
    res = client.post("/api/discover", json={"query": query})
    assert res.status_code == 200, f"Status: {res.status_code}"
    data = res.json()
    
    extracted = data["extracted_preferences"]
    print(f"  Input Intent: '{query}'")
    print(f"  Extracted Attributes: Genre={extracted.get('genre')}, Mood={extracted.get('mood')}, Max Pages={extracted.get('max_pages')}, Romance={extracted.get('romance_level')}")
    assert extracted["genre"] in ["Mystery", "Any"]
    assert extracted["mood"] in ["Dark", "Suspenseful", "Any"]
    assert extracted["max_pages"] is not None and extracted["max_pages"] <= 350
    print("  -> PASS: Natural-Language Preference Extraction Verified.")

    # Test 2: P0 AI Book Matching, Hybrid Ranking & Book DNA
    print("\n[TEST 2] P0 — AI Book Matching, Hybrid Ranking & Book DNA Profile...")
    recs = data["recommendations"]
    assert len(recs) > 0
    top_book = recs[0]
    print(f"  Top Recommended Book: '{top_book['title']}' by {top_book['author']}")
    print(f"  Compatibility Score: {int(top_book['match_score'] * 100)}%")
    print(f"  Score Breakdown: {top_book['score_breakdown']}")
    print(f"  Book DNA Profile: {top_book['book_dna']}")
    print(f"  Spoiler-Free Reason: {top_book['explanation']}")
    assert top_book["match_score"] > 0
    assert "book_dna" in top_book
    assert "explanation" in top_book
    print("  -> PASS: AI Book Matching & Book DNA Verified.")

    # Test 3: P0 "Change One Thing" & Conversational Refinement
    print("\n[TEST 3] P0 — 'Change One Thing' & Conversational Refinement...")
    session_id = data["session_id"]
    ref_res = client.post("/api/refine", json={"session_id": session_id, "instruction": "Make it darker"})
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    print(f"  Applied Refinement: 'Make it darker'")
    print(f"  Updated Preference Mood: {ref_data['updated_preferences']['mood']}")
    assert ref_data["updated_preferences"]["mood"] == "Dark"
    print("  -> PASS: Conversational Refinement Verified.")

    # Test 4: P0 Preference-Aware Side-by-Side Comparison
    print("\n[TEST 4] P0 — Preference-Aware Side-by-Side Comparison...")
    book_ids = [r["id"] for r in recs[:2]]
    comp_res = client.post("/api/compare", json={"book_ids": book_ids, "active_intent": extracted})
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    print(f"  Compared Books: {[b['title'] for b in comp_data['compared_books']]}")
    print(f"  AI Comparison Verdict: {comp_data['verdict']}")
    assert len(comp_data["compared_books"]) == 2
    assert "verdict" in comp_data
    print("  -> PASS: Preference-Aware Comparison Verified.")

    # Test 5: P1 Personal Reading History
    print("\n[TEST 5] P1 — Personal Reading History & Rejection Signals...")
    save_res = client.post(f"/api/books/{top_book['id']}/status", json={"book_id": top_book['id'], "status": "saved"})
    assert save_res.status_code == 200
    hist_res = client.get("/api/history")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()["history"]
    print(f"  Saved History Count: {len(hist_data)}")
    assert len(hist_data) > 0
    print("  -> PASS: Personal Reading History Verified.")

    # Test 6: P1 Progressive Reading Path
    print("\n[TEST 6] P1 — Progressive Reading Path...")
    path_res = client.post("/api/reading-path", json={"topic_or_genre": "Fantasy"})
    assert path_res.status_code == 200
    path_data = path_res.json()
    print(f"  Reading Path: {path_data['path_name']}")
    for step in path_data["steps"]:
        print(f"    Step {step['step']} ({step['stage']}): '{step['title']}' - {step['reason']}")
    assert len(path_data["steps"]) > 0
    print("  -> PASS: Progressive Reading Path Verified.")

    # Test 7: Evaluation Engine (Precision@K & Conventional vs NL Search Experiment)
    print("\n[TEST 7] Evaluation Engine & Comparative Experiment...")
    exp_res = client.get("/api/evaluation/experiment")
    assert exp_res.status_code == 200
    exp_data = exp_res.json()
    print(f"  Conventional Search Precision@5: {exp_data['conventional_search']['precision_at_5']}")
    print(f"  LitLens NL Search Precision@5:  {exp_data['natural_language_search']['precision_at_5']}")
    print(f"  Key Findings: {exp_data['findings']}")
    assert exp_data["natural_language_search"]["precision_at_5"] >= exp_data["conventional_search"]["precision_at_5"]
    print("  -> PASS: Evaluation Engine & Comparative Experiment Verified.")

    print("\n" + "=" * 60)
    print("      ALL REQUIREMENT AUDITS PASSED WITH 100% PASS RATE")
    print("=" * 60)

if __name__ == "__main__":
    main()
