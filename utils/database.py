# utils/database.py
import sqlite3
import json
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db")
DB_PATH = os.path.join(DB_DIR, "sessions.db")

def init_db():
    """Initialize the SQLite database and create tables if they do not exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Sessions table (stores trust score & mode)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            trust_score INTEGER DEFAULT 100,
            mode TEXT DEFAULT 'NORMAL',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Messages table (stores chat history)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
        )
    """)
    
    # 3. Learning Queue table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            retrieved_context TEXT,
            confidence INTEGER,
            status TEXT DEFAULT 'pending',
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def get_session_score_and_mode(session_id: str) -> tuple[int, str]:
    """Get the trust score and mode for a session. Initializes session if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT trust_score, mode FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0], row[1]
    
    # Initialize session
    set_session_score_and_mode(session_id, 100, "NORMAL")
    return 100, "NORMAL"

def set_session_score_and_mode(session_id: str, score: int, mode: str):
    """Upsert trust score and mode for a session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (session_id, trust_score, mode, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            trust_score = excluded.trust_score,
            mode = excluded.mode,
            updated_at = CURRENT_TIMESTAMP
    """, (session_id, score, mode))
    conn.commit()
    conn.close()

def get_session_history(session_id: str) -> list[dict]:
    """Get conversation history for a session formatted for Ollama/LLM."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [{"role": r, "content": c} for r, c in rows]

def get_session_history_with_timestamps(session_id: str) -> list[dict]:
    """Get history with timestamps (for UI display)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role, content, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": str(row[0]),
            "role": row[1],
            "content": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]

def add_message(session_id: str, role: str, content: str, timestamp: str = None) -> int:
    """Add a message to the session's history."""
    if not timestamp:
        timestamp = datetime.now().strftime("%I:%M %p")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure session exists in the sessions table
    cursor.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))
    
    cursor.execute("""
        INSERT INTO messages (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, role, content, timestamp))
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return msg_id

def reset_session_db(session_id: str):
    """Clear history and reset trust score to 100 for a session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("UPDATE sessions SET trust_score = 100, mode = 'NORMAL' WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def reset_all_sessions_db():
    """Clear all sessions, message history, and learning queue items."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM sessions")
    cursor.execute("DELETE FROM learning_queue")
    conn.commit()
    conn.close()

# --- Learning Queue Database Operations ---

def log_gap_db(question: str, retrieved_context: list, confidence: int) -> dict:
    """Log a knowledge gap to the database. Prevents duplicate questions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check for duplicates
    cursor.execute("SELECT id, status FROM learning_queue WHERE LOWER(TRIM(question)) = LOWER(TRIM(?))", (question,))
    row = cursor.fetchone()
    
    context_str = json.dumps(retrieved_context)
    
    if row:
        conn.close()
        return {
            "message": "Question already exists",
            "existing_id": row[0],
            "status": row[1]
        }
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO learning_queue (question, retrieved_context, confidence, status, timestamp)
        VALUES (?, ?, ?, 'pending', ?)
    """, (question, context_str, confidence, timestamp))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": item_id,
        "question": question,
        "retrieved_context": retrieved_context,
        "confidence": confidence,
        "status": "pending",
        "timestamp": timestamp
    }

def get_learning_queue_db() -> list[dict]:
    """Retrieve all items in the learning queue."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, retrieved_context, confidence, status, timestamp FROM learning_queue ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for r in rows:
        try:
            ctx = json.loads(r[2])
        except:
            ctx = []
        items.append({
            "id": r[0],
            "question": r[1],
            "retrieved_context": ctx,
            "confidence": r[3],
            "status": r[4],
            "timestamp": r[5]
        })
    return items

def update_learning_queue_status_db(item_id: int, status: str) -> bool:
    """Update status of a learning queue item (e.g. approved, rejected)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE learning_queue SET status = ? WHERE id = ?", (status, item_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def get_learning_queue_item_db(item_id: int) -> dict:
    """Get a single learning queue item."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, retrieved_context, confidence, status, timestamp FROM learning_queue WHERE id = ?", (item_id,))
    r = cursor.fetchone()
    conn.close()
    
    if r:
        try:
            ctx = json.loads(r[2])
        except:
            ctx = []
        return {
            "id": r[0],
            "question": r[1],
            "retrieved_context": ctx,
            "confidence": r[3],
            "status": r[4],
            "timestamp": r[5]
        }
    return None

# Initialize on import
init_db()
