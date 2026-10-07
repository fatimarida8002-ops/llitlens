import json
import uuid
import random
import urllib.parse
import requests
from typing import List, Dict, Any
from app.db.database import get_db_connection, execute_db, query_db

CURATED_SEED_BOOKS = [
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "genre": "Mystery",
        "subgenre": "Psychological Thriller",
        "pages": 422,
        "publication_year": 2012,
        "description": "On their fifth wedding anniversary, Nick Dunne's wife Amy suddenly disappears. Under pressure from the police and a growing media frenzy, Nick's portrait of a blissful marriage begins to crumble, revealing dark secrets and deception.",
        "mood": "Dark",
        "pacing": "Fast",
        "romance_level": "Low",
        "complexity": "Medium",
        "emotional_intensity": "High",
        "setting": "Suburban Missouri",
        "themes": "Deception, Marriage, Identity, Media Frenzy, Revenge",
        "cover_url": "https://covers.openlibrary.org/b/id/8231996-L.jpg"
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "genre": "Mystery",
        "subgenre": "Psychological Thriller",
        "pages": 325,
        "publication_year": 2019,
        "description": "Alicia Berenson's life is seemingly perfect. One evening her husband returns late, and Alicia shoots him five times in the face and then never speaks another word. Theo Faber, a criminal psychotherapist, is determined to unravel her motive.",
        "mood": "Suspenseful",
        "pacing": "Fast",
        "romance_level": "None",
        "complexity": "Medium",
        "emotional_intensity": "High",
        "setting": "Psychiatric Facility, London",
        "themes": "Trauma, Silence, Obsession, Psychological Secrets",
        "cover_url": "https://covers.openlibrary.org/b/id/10522434-L.jpg"
    },
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "genre": "Sci-Fi",
        "subgenre": "Space Exploration",
        "pages": 496,
        "publication_year": 2021,
        "description": "Ryland Grace is the sole survivor on a desperate, last-chance mission to save humanity from an extinction-level solar crisis. The only problem is he just woke up from a coma with complete amnesia.",
        "mood": "Thought-provoking",
        "pacing": "Fast",
        "romance_level": "None",
        "complexity": "Medium",
        "emotional_intensity": "High",
        "setting": "Interstellar Space",
        "themes": "Science, Survival, Unlikely Friendship, Ingenuity",
        "cover_url": "https://covers.openlibrary.org/b/id/10531520-L.jpg"
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Sci-Fi",
        "subgenre": "Epic Sci-Fi",
        "pages": 688,
        "publication_year": 1965,
        "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only commodity of value is the spice melange.",
        "mood": "Dark",
        "pacing": "Slow",
        "romance_level": "Low",
        "complexity": "High",
        "emotional_intensity": "High",
        "setting": "Arrakis Desert World",
        "themes": "Politics, Religion, Ecology, Power, Destiny",
        "cover_url": "https://covers.openlibrary.org/b/id/8100913-L.jpg"
    },
    {
        "title": "The House in the Cerulean Sea",
        "author": "TJ Klune",
        "genre": "Fantasy",
        "subgenre": "Cozy Fantasy",
        "pages": 396,
        "publication_year": 2020,
        "description": "Linus Baker is a by-the-book caseworker at the Department in Charge of Magical Youth. He is sent to investigate an isolated orphanage housing six dangerous magical children and their charismatic caretaker.",
        "mood": "Comforting",
        "pacing": "Medium",
        "romance_level": "Low",
        "complexity": "Easy",
        "emotional_intensity": "Medium",
        "setting": "Seaside Orphanage",
        "themes": "Found Family, Acceptance, Kindheartedness, Belonging",
        "cover_url": "https://covers.openlibrary.org/b/id/10323382-L.jpg"
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genre": "Fantasy",
        "subgenre": "Epic Fantasy",
        "pages": 662,
        "publication_year": 2007,
        "description": "Told in Kvothe's own voice, this is the story of the magically gifted young man who grows to be the most notorious wizard his world has ever seen.",
        "mood": "Atmospheric",
        "pacing": "Medium",
        "romance_level": "Low",
        "complexity": "High",
        "emotional_intensity": "High",
        "setting": "The University, Temerant",
        "themes": "Magic, Storytelling, Grief, Knowledge, Music",
        "cover_url": "https://covers.openlibrary.org/b/id/8226191-L.jpg"
    },
    {
        "title": "Piranesi",
        "author": "Susanna Clarke",
        "genre": "Fantasy",
        "subgenre": "Low Fantasy / Mystery",
        "pages": 245,
        "publication_year": 2020,
        "description": "Piranesi lives in the House. Perhaps he has always lived there. Day after day he explores endless halls lined with thousands of statues while tides sweep through lower rooms.",
        "mood": "Mysterious",
        "pacing": "Medium",
        "romance_level": "None",
        "complexity": "Medium",
        "emotional_intensity": "Medium",
        "setting": "Infinite Labyrinthine Palace",
        "themes": "Isolation, Wonder, Memory, Innocence",
        "cover_url": "https://covers.openlibrary.org/b/id/10385966-L.jpg"
    },
    {
        "title": "The Night Circus",
        "author": "Erin Morgenstern",
        "genre": "Fantasy",
        "subgenre": "Historical Fantasy",
        "pages": 387,
        "publication_year": 2011,
        "description": "Le Cirque des Rêves arrives without warning. Within its black-and-white striped canvas tents is an utterly unique experience full of breathtaking amazements. Behind the scenes, a fierce competition is underway.",
        "mood": "Atmospheric",
        "pacing": "Medium",
        "romance_level": "Medium",
        "complexity": "Medium",
        "emotional_intensity": "Medium",
        "setting": "Victorian Travelling Circus",
        "themes": "Magic, Rivalry, Illusion, Romance",
        "cover_url": "https://covers.openlibrary.org/b/id/7288673-L.jpg"
    },
    {
        "title": "And Then There Were None",
        "author": "Agatha Christie",
        "genre": "Mystery",
        "subgenre": "Classic Whodunit",
        "pages": 272,
        "publication_year": 1939,
        "description": "Ten strangers are lured to an isolated island off the Devon coast by a mysterious host. One by one, they are accused of past crimes and mysteriously murdered according to a nursery rhyme.",
        "mood": "Suspenseful",
        "pacing": "Fast",
        "romance_level": "None",
        "complexity": "Easy",
        "emotional_intensity": "High",
        "setting": "Isolated Soldier Island",
        "themes": "Guilt, Retribution, Paranoia, Justice",
        "cover_url": "https://covers.openlibrary.org/b/id/8235118-L.jpg"
    },
    {
        "title": "A Man Called Ove",
        "author": "Fredrik Backman",
        "genre": "Literary",
        "subgenre": "Contemporary Fiction",
        "pages": 337,
        "publication_year": 2012,
        "description": "Ove is a curmudgeonly old man who enforces neighborhood rules with strict precision. Behind his grumpy exterior lies a heartbreaking story of love and loss that changes when noisy new neighbors move in.",
        "mood": "Uplifting",
        "pacing": "Medium",
        "romance_level": "Low",
        "complexity": "Easy",
        "emotional_intensity": "High",
        "setting": "Swedish Neighborhood",
        "themes": "Community, Grief, Friendship, Second Chances",
        "cover_url": "https://covers.openlibrary.org/b/id/8233321-L.jpg"
    },
    {
        "title": "Klara and the Sun",
        "author": "Kazuo Ishiguro",
        "genre": "Sci-Fi",
        "subgenre": "Dystopian / Literary",
        "pages": 303,
        "publication_year": 2021,
        "description": "Klara is an Artificial Friend with outstanding observational qualities, who, from her place in the store, watches carefully the behavior of those who come in to browse.",
        "mood": "Thought-provoking",
        "pacing": "Medium",
        "romance_level": "None",
        "complexity": "Medium",
        "emotional_intensity": "High",
        "setting": "Near-future America",
        "themes": "Artificial Intelligence, Love, Morality, Devotion",
        "cover_url": "https://covers.openlibrary.org/b/id/10542381-L.jpg"
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "genre": "Sci-Fi",
        "subgenre": "Cyberpunk",
        "pages": 271,
        "publication_year": 1984,
        "description": "Case was the hottest computer cowboy cruising the information superhighway until he crossed the wrong people. Now an enigmatic employer hires him for a last-chance run against an unthinkably powerful AI.",
        "mood": "Dark",
        "pacing": "Fast",
        "romance_level": "Low",
        "complexity": "High",
        "emotional_intensity": "Medium",
        "setting": "Chiba City, Cyberspace",
        "themes": "Cyberpunk, Technology, Identity, Consciousness",
        "cover_url": "https://covers.openlibrary.org/b/id/8225266-L.jpg"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "subgenre": "High Fantasy",
        "pages": 310,
        "publication_year": 1937,
        "description": "Bilbo Baggins is a hobbit who enjoys a comfortable, unambitious life. His contentment is disturbed when the wizard Gandalf and a company of thirteen dwarves arrive to enlist him on a quest to reclaim their stolen dragon hoard.",
        "mood": "Adventurous",
        "pacing": "Medium",
        "romance_level": "None",
        "complexity": "Easy",
        "emotional_intensity": "Medium",
        "setting": "Middle-earth",
        "themes": "Courage, Quest, Friendship, Greed",
        "cover_url": "https://covers.openlibrary.org/b/id/8406786-L.jpg"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": "Sci-Fi",
        "subgenre": "Dystopian",
        "pages": 328,
        "publication_year": 1949,
        "description": "Winston Smith rewrites history for the Ministry of Truth. Outwardly a conformist, Winston dreams of rebellion against Big Brother and falls in love with Julia in a totalitarian regime where thoughtcrime is punishable by death.",
        "mood": "Dark",
        "pacing": "Medium",
        "romance_level": "Low",
        "complexity": "Medium",
        "emotional_intensity": "High",
        "setting": "Airstrip One, Oceania",
        "themes": "Totalitarianism, Surveillance, Truth, Control",
        "cover_url": "https://covers.openlibrary.org/b/id/7222246-L.jpg"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "Romance",
        "subgenre": "Classic Romance",
        "pages": 279,
        "publication_year": 1813,
        "description": "Elizabeth Bennet navigates issues of manners, upbringing, morality, education, and marriage in the landed gentry society of early 19th-century England, clashing with the proud Mr. Darcy.",
        "mood": "Funny",
        "pacing": "Medium",
        "romance_level": "High",
        "complexity": "Medium",
        "emotional_intensity": "Medium",
        "setting": "Regency England",
        "themes": "Class, Prejudice, Family, Wit, Love",
        "cover_url": "https://covers.openlibrary.org/b/id/8225261-L.jpg"
    },
    {
        "title": "Beach Read",
        "author": "Emily Henry",
        "genre": "Romance",
        "subgenre": "Contemporary Romance",
        "pages": 361,
        "publication_year": 2020,
        "description": "A romance writer who no longer believes in love and a literary writer stuck in a rut engage in a summer-long challenge that may just overturn everything they believe about their stories and themselves.",
        "mood": "Uplifting",
        "pacing": "Fast",
        "romance_level": "High",
        "complexity": "Easy",
        "emotional_intensity": "Medium",
        "setting": "Lake Michigan Beach Town",
        "themes": "Grief, Writers, Love, Humor, Personal Growth",
        "cover_url": "https://covers.openlibrary.org/b/id/10398672-L.jpg"
    }
]

def seed_books_to_db():
    conn = get_db_connection()
    try:
        for b in CURATED_SEED_BOOKS:
            book_id = f"book_{uuid.uuid4().hex[:12]}"
            ext_id = f"OL_{b['title'].lower().replace(' ', '_')}"
            
            # Check if book title already exists
            existing = conn.execute("SELECT id FROM books WHERE title = ?", (b['title'],)).fetchone()
            if existing:
                b_id = existing['id']
            else:
                b_id = book_id
                # Insert book
                conn.execute(
                    """INSERT INTO books 
                    (id, external_id, title, author, description, pages, publication_year, cover_url, source) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (b_id, ext_id, b['title'], b['author'], b['description'], b['pages'], b['publication_year'], b['cover_url'], 'open_library')
                )
            
            # Insert Author
            author_id = f"auth_{uuid.uuid4().hex[:8]}"
            conn.execute("INSERT OR IGNORE INTO authors (id, name) VALUES (?, ?)", (author_id, b['author']))
            author_rec = conn.execute("SELECT id FROM authors WHERE name = ?", (b['author'],)).fetchone()
            if author_rec:
                conn.execute("INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)", (b_id, author_rec['id']))
                
            # Insert Genre
            genre_id = f"gen_{uuid.uuid4().hex[:8]}"
            conn.execute("INSERT OR IGNORE INTO genres (id, name) VALUES (?, ?)", (genre_id, b['genre']))
            genre_rec = conn.execute("SELECT id FROM genres WHERE name = ?", (b['genre'],)).fetchone()
            if genre_rec:
                conn.execute("INSERT OR IGNORE INTO book_genres (book_id, genre_id) VALUES (?, ?)", (b_id, genre_rec['id']))
                
            # Insert Book DNA Attributes
            attr_json = json.dumps({
                "mood": b['mood'],
                "pacing": b['pacing'],
                "romance_level": b['romance_level'],
                "complexity": b['complexity'],
                "emotional_intensity": b['emotional_intensity'],
                "setting": b['setting'],
                "themes": b['themes']
            })
            
            conn.execute(
                """INSERT OR REPLACE INTO book_attributes 
                (book_id, mood, pacing, romance_level, complexity, emotional_intensity, setting, themes, attributes_json, confidence) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (b_id, b['mood'], b['pacing'], b['romance_level'], b['complexity'], b['emotional_intensity'], b['setting'], b['themes'], attr_json, 0.95)
            )

            # Seed Verified Baseline Availability Links ("Where to Get It")
            q_title_author = urllib.parse.quote(f"{b['title']} {b['author']}")
            ol_search_url = f"https://openlibrary.org/search?q={q_title_author}"
            gb_search_url = f"https://www.google.com/search?tbm=bks&q={q_title_author}"
            amz_search_url = f"https://www.amazon.com/s?k={q_title_author}&i=stripbooks"

            avail_records = [
                ("Open Library", "read_borrow", ol_search_url),
                ("Google Books", "buy", gb_search_url),
                ("Amazon", "buy", amz_search_url)
            ]

            for prov_name, prov_type, url in avail_records:
                avail_id = f"avail_{uuid.uuid4().hex[:12]}"
                conn.execute(
                    """INSERT OR IGNORE INTO book_availability 
                    (id, book_id, provider_name, provider_type, url, is_verified) 
                    VALUES (?, ?, ?, ?, ?, 1)""",
                    (avail_id, b_id, prov_name, prov_type, url)
                )

        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    from app.db.database import init_db
    init_db()
    seed_books_to_db()
    print("Curated seed book dataset & availability links ingested successfully.")
