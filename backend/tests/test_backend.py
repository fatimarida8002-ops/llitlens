import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db, ensure_default_user
from app.ingestion.open_library import seed_books_to_db
from app.services.ai_provider import ai_provider

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    ensure_default_user()
    seed_books_to_db()

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_preference_extraction():
    query = "I want a dark mystery under 300 pages with a huge plot twist and almost no romance."
    prefs = ai_provider.extract_preferences(query)
    assert prefs["genre"] in ["Mystery", "Any"]
    assert prefs["mood"] in ["Dark", "Suspenseful", "Any"]
    assert prefs["max_pages"] is not None and prefs["max_pages"] <= 350

def test_discover_api():
    payload = {"query": "I want a cozy fantasy book with low romance"}
    response = client.post("/api/discover", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["recommendations"]) > 0
    top_rec = data["recommendations"][0]
    assert "match_score" in top_rec
    assert "book_dna" in top_rec
    assert "explanation" in top_rec

def test_refine_api():
    disc_res = client.post("/api/discover", json={"query": "I want a mystery novel"})
    session_id = disc_res.json()["session_id"]
    
    ref_res = client.post("/api/refine", json={"session_id": session_id, "instruction": "Make it darker"})
    assert ref_res.status_code == 200
    ref_data = ref_res.json()
    assert ref_data["updated_preferences"]["mood"] == "Dark"

def test_evaluation_experiment_api():
    response = client.get("/api/evaluation/experiment")
    assert response.status_code == 200
    data = response.json()
    assert "conventional_search" in data
    assert "natural_language_search" in data
