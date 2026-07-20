# models/schemas.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    username: Optional[str] = "user"

class ChatResponse(BaseModel):
    reply: str
    intent: str
    session_id: str
    trust_score: Optional[float] = None
    confidence_score: Optional[float] = None
    mode: Optional[str] = None        # "NORMAL", "CAUTIOUS", or "LOCKDOWN"
    events: list = []
    # Product Intelligence fields (only populated when intent == PRODUCT_INTEL)
    route: Optional[str] = None                     # pain_points | prioritization | roadmap | competitor | fallback
    sources: Optional[list[dict]] = None            # retrieved evidence metadata
    priority_table: Optional[list[dict]] = None     # scoring table (prioritization route only)