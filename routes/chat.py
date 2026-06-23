# routes/chat.py
from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from utils.session_store import get_session, add_to_session

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Get or create the session history
    history = get_session(request.session_id)

    # 2. Store the user's message in session
    add_to_session(request.session_id, "user", request.message)

    # 3. Hardcoded reply for now — swap for real Ollama call on Day 3
    reply = f"[Day 2 placeholder] You said: '{request.message}'. LLM integration coming Day 3."

    # 4. Store the bot's reply in session
    add_to_session(request.session_id, "assistant", reply)

    return ChatResponse(
        reply=reply,
        session_id=request.session_id,
        events=["Hardcoded response returned", f"Session '{request.session_id}' has {len(history)} messages"]
    )