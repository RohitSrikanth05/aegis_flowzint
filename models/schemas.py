# models/schemas.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    reply: str
    intent: str
    session_id: str
    trust_score: Optional[float] = None
    confidence_score: Optional[float] = None
    mode: Optional[str] = None        # "NORMAL", "CAUTIOUS", or "LOCKDOWN"
    events: list = []