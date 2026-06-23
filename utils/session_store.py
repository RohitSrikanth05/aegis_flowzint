# utils/session_store.py

sessions: dict = {}

def get_session(session_id: str) -> list:
    """Return the message history for a session. Creates it if it doesn't exist."""
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]

def add_to_session(session_id: str, role: str, content: str):
    """Append a message to a session's history."""
    sessions[session_id].append({"role": role, "content": content})

def reset_session(session_id: str):
    """Clear a session (useful for demo resets later)."""
    sessions[session_id] = []