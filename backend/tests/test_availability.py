import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db, ensure_default_user, query_db
from app.ingestion.open_library import seed_books_to_db
from app.services.availability import availability_resolver

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    ensure_default_user()
    seed_books_to_db()

def test_book_availability_resolution():
    book = query_db("SELECT id, title FROM books LIMIT 1", one=True)
    assert book is not None
    
    avail = availability_resolver.get_availability(book["id"])
    assert isinstance(avail, list)
    assert len(avail) >= 1
    
    first = avail[0]
    assert "provider_name" in first
    assert "provider_type" in first
    assert "url" in first
    assert first["url"].startswith("http")

def test_url_security_validation():
    assert availability_resolver._is_valid_url("https://openlibrary.org/works/OL12345W") is True
    assert availability_resolver._is_valid_url("https://books.google.com/books?id=123") is True
    assert availability_resolver._is_valid_url("https://www.amazon.com/s?k=test") is True
    assert availability_resolver._is_valid_url("http://malicious-phishing-site.org") is False
    assert availability_resolver._is_valid_url("javascript:alert(1)") is False

def test_availability_api_endpoint():
    book = query_db("SELECT id FROM books LIMIT 1", one=True)
    response = client.get(f"/api/books/{book['id']}/availability")
    assert response.status_code == 200
    data = response.json()
    assert "book_id" in data
    assert "availability" in data
    assert len(data["availability"]) >= 1

def test_discover_api_includes_availability():
    response = client.post("/api/discover", json={"query": "cozy fantasy book"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0
    top_rec = data["recommendations"][0]
    assert "availability" in top_rec
    assert len(top_rec["availability"]) >= 1

def test_graceful_empty_availability():
    # Non-existent or newly created book with no availability records
    fake_id = "book_non_existent_1234"
    avail = availability_resolver.get_availability(fake_id)
    assert avail == []
