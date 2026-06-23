# models/schemas.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"   # optional — defaults to "default" for now

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    intent: str = "UNKNOWN"         # Swathi fills this in on Day 3
    trust_score: float = 100.0      # Unnathi fills this in on Day 6
    confidence_score: float = 0.0   # Rohit fills this in on Day 5
    events: list[str] = []          # running log of what happened this turn