-- LitLens Database Schema (PostgreSQL & SQLite Compatible)

CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    external_id TEXT UNIQUE,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    pages INTEGER DEFAULT 300,
    publication_year INTEGER,
    cover_url TEXT,
    source TEXT DEFAULT 'open_library',
    vector_json TEXT, -- Serialized embedding vector for semantic search
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS authors (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS genres (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS book_genres (
    book_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

-- Book DNA Profile Attributes
CREATE TABLE IF NOT EXISTS book_attributes (
    book_id TEXT PRIMARY KEY,
    mood TEXT NOT NULL DEFAULT 'Balanced',
    pacing TEXT NOT NULL DEFAULT 'Medium',
    romance_level TEXT NOT NULL DEFAULT 'Medium',
    complexity TEXT NOT NULL DEFAULT 'Medium',
    emotional_intensity TEXT NOT NULL DEFAULT 'Medium',
    setting TEXT DEFAULT 'General',
    themes TEXT, -- Comma-separated or JSON list
    attributes_json TEXT, -- Complete structured DNA breakdown
    confidence REAL DEFAULT 0.9,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Verified Book Availability & Access Links ("Where to Get It")
CREATE TABLE IF NOT EXISTS book_availability (
    id TEXT PRIMARY KEY,
    book_id TEXT NOT NULL,
    provider_name TEXT NOT NULL, -- e.g. 'Open Library', 'Google Books', 'Amazon'
    provider_type TEXT NOT NULL, -- e.g. 'read_borrow', 'buy'
    url TEXT NOT NULL,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified INTEGER DEFAULT 1,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    UNIQUE(book_id, provider_name, provider_type)
);

-- User Profiles
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Personal Reading History & Interactions
CREATE TABLE IF NOT EXISTS user_books (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    book_id TEXT NOT NULL,
    status TEXT CHECK(status IN ('saved', 'reading', 'read', 'rejected')) NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Persistent User Preferences
CREATE TABLE IF NOT EXISTS user_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    attribute TEXT NOT NULL,
    value TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    source TEXT DEFAULT 'explicit',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Recommendation Sessions & Conversational Refinement
CREATE TABLE IF NOT EXISTS recommendation_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    original_query TEXT NOT NULL,
    current_preferences_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS conversation_turns (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    extracted_preferences_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES recommendation_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    book_id TEXT NOT NULL,
    match_score REAL NOT NULL,
    rank INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES recommendation_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Create Performance Indexes
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON books(author);
CREATE INDEX IF NOT EXISTS idx_user_books_user_status ON user_books(user_id, status);
CREATE INDEX IF NOT EXISTS idx_recommendations_session ON recommendations(session_id);
CREATE INDEX IF NOT EXISTS idx_book_availability_book ON book_availability(book_id);
