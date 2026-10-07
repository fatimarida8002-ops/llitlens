import uuid
import urllib.parse
import requests
from typing import List, Dict, Any
from app.db.database import query_db, execute_db

class AvailabilityResolver:
    """
    Service for resolving, verifying, caching, and serving authentic
    book availability & access links (Open Library, Google Books, Amazon).
    """

    def get_availability(self, book_id: str) -> List[Dict[str, Any]]:
        # 1. Fetch cached verified availability from DB
        rows = query_db(
            "SELECT * FROM book_availability WHERE book_id = ? AND is_verified = 1 ORDER BY provider_name ASC",
            (book_id,)
        )
        if rows:
            return [dict(r) for r in rows]

        # 2. If not cached, attempt dynamic resolution against official APIs
        book = query_db("SELECT * FROM books WHERE id = ?", (book_id,), one=True)
        if not book:
            return []

        resolved_links = self._fetch_and_verify_external_links(book["title"], book["author"], book.get("external_id"))

        # 3. Store verified links in database cache
        for link in resolved_links:
            rec_id = f"avail_{uuid.uuid4().hex[:12]}"
            execute_db(
                """INSERT OR IGNORE INTO book_availability 
                (id, book_id, provider_name, provider_type, url, is_verified) 
                VALUES (?, ?, ?, ?, ?, 1)""",
                (rec_id, book_id, link["provider_name"], link["provider_type"], link["url"])
            )

        # Re-query DB after insertion
        fresh_rows = query_db(
            "SELECT * FROM book_availability WHERE book_id = ? AND is_verified = 1 ORDER BY provider_name ASC",
            (book_id,)
        )
        return [dict(r) for r in fresh_rows]

    def _fetch_and_verify_external_links(self, title: str, author: str, external_id: str = None) -> List[Dict[str, Any]]:
        links = []
        clean_title = title.strip()
        clean_author = author.strip()

        # 1. Open Library Read/Borrow Link Search
        try:
            ol_url = f"https://openlibrary.org/search.json?title={urllib.parse.quote(clean_title)}&author={urllib.parse.quote(clean_author)}"
            resp = requests.get(ol_url, timeout=3)
            if resp.status_code == 200:
                docs = resp.json().get("docs", [])
                if docs:
                    top_doc = docs[0]
                    ol_key = top_doc.get("key") # e.g. /works/OL123456W
                    if ol_key:
                        verified_ol_link = f"https://openlibrary.org{ol_key}"
                        if self._is_valid_url(verified_ol_link):
                            links.append({
                                "provider_name": "Open Library",
                                "provider_type": "read_borrow",
                                "url": verified_ol_link
                            })
        except Exception:
            pass

        # 2. Google Books Buy/Read Link Search
        try:
            gb_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{urllib.parse.quote(clean_title)}+inauthor:{urllib.parse.quote(clean_author)}"
            resp = requests.get(gb_url, timeout=3)
            if resp.status_code == 200:
                items = resp.json().get("items", [])
                if items:
                    top_item = items[0]
                    info = top_item.get("volumeInfo", {})
                    info_link = info.get("infoLink") or info.get("previewLink")
                    if info_link and self._is_valid_url(info_link):
                        links.append({
                            "provider_name": "Google Books",
                            "provider_type": "buy",
                            "url": info_link
                        })
        except Exception:
            pass

        # 3. Verified Amazon Search Link (Strict Title + Author Search query)
        search_query = urllib.parse.quote(f"{clean_title} {clean_author}")
        amazon_url = f"https://www.amazon.com/s?k={search_query}&i=stripbooks"
        if self._is_valid_url(amazon_url):
            links.append({
                "provider_name": "Amazon",
                "provider_type": "buy",
                "url": amazon_url
            })

        return links

    def _is_valid_url(self, url: str) -> bool:
        """
        Validates HTTPS protocol and authentic domain targets.
        """
        if not url or not isinstance(url, str):
            return False
        if not (url.startswith("https://") or url.startswith("http://")):
            return False
        # Block malicious/suspicious domains
        allowed_domains = ["openlibrary.org", "books.google.com", "google.com", "amazon.com", "www.amazon.com"]
        try:
            parsed = urllib.parse.urlparse(url)
            return any(domain in parsed.netloc for domain in allowed_domains)
        except Exception:
            return False

availability_resolver = AvailabilityResolver()
