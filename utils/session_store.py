# utils/session_store.py

_sessions: dict[str, list] = {}

def get_session(session_id: str) -> list:
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]

def update_session(session_id: str, history: list):
    _sessions[session_id] = history

def add_to_session(session_id: str, role: str, content: str):
    """Append a message to a session's history."""
    sessions[session_id].append({"role": role, "content": content})

def reset_session(session_id: str):
    """Clear a session (useful for demo resets later)."""
    sessions[session_id] = []