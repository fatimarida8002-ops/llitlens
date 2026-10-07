import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.config import settings, DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    conn = get_db_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

def query_db(query: str, args: tuple = (), one: bool = False) -> Any:
    conn = get_db_connection()
    try:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

def execute_db(query: str, args: tuple = ()) -> int:
    conn = get_db_connection()
    try:
        cur = conn.execute(query, args)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()

# Seed default user if not existing
def ensure_default_user():
    user = query_db("SELECT * FROM users WHERE id = ?", ("default_user",), one=True)
    if not user:
        execute_db(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            ("default_user", "Default Reader", "reader@litlens.app")
        )
