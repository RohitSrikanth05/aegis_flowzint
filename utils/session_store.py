# utils/session_store.py
import sqlite3
from utils.database import DB_PATH, get_session_history, add_message, reset_session_db

def get_session(session_id: str) -> list:
    """Retrieve session history from SQLite database."""
    return get_session_history(session_id)

def update_session(session_id: str, history: list):
    """Sync session history to SQLite database by rewriting messages."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    for msg in history:
        cursor.execute(
            "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, msg.get("role"), msg.get("content"), msg.get("timestamp"))
        )
    conn.commit()
    conn.close()

def add_to_session(session_id: str, role: str, content: str):
    """Append a single message to a session's history."""
    add_message(session_id, role, content)

def reset_session(session_id: str):
    """Clear a session's history and reset its trust score to 100."""
    reset_session_db(session_id)