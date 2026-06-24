# routes/chat.py
import asyncio
from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.ollama_client import chat_with_ollama, classify_intent
from utils.session_store import get_session, update_session

# Unnathi's modules
from services.trust_engine.detector import TrustDetector
from services.trust_engine.scorer import TrustScorer
from services.trust_engine.logger import TrustLogger
from services.trust_engine.escalation import TrustEscalation

router = APIRouter()

# One instance per application (they manage state per session_id internally)
detector = TrustDetector()
scorer = TrustScorer()
logger = TrustLogger()
escalation = TrustEscalation()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or "default"
    user_message = request.message
    events = []

    # ── 1. Initialize trust session if first message ──────────────────────
    scorer.initialize_session(session_id)

    # ── 2. Threat detection ───────────────────────────────────────────────
    threats = detector.analyze(user_message)

    # ── 3. Trust scoring ──────────────────────────────────────────────────
    if threats:
        result = scorer.apply_threat_deduction(session_id, threats)
        logger.log_threat_detection(
            session_id, user_message, threats,
            result["score_before"], result["score_after"]
        )
        events.append(f"Threats detected: {', '.join(threats)}")
        events.append(f"Trust score dropped: {result['score_before']} → {result['score_after']}")
    else:
        result = scorer.apply_clean_message_recovery(session_id)
        logger.log_clean_message(
            session_id, user_message,
            result["score_before"], result["score_after"]
        )

    trust_score = result["score_after"]
    mode = result["mode"]

    if mode != "NORMAL":
        events.append(f"Session mode: {mode}")

    # ── 4. Get mode-specific system prompt ────────────────────────────────
    system_prompt = escalation.get_system_prompt(mode)

    # ── 5. Build conversation history with system prompt injected ─────────
    history = get_session(session_id)
    messages_with_system = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": user_message}]
    )

    # ── 6. LLM reply + intent classification concurrently ─────────────────
    try:
        reply, intent = await asyncio.gather(
            chat_with_ollama(messages_with_system),
            classify_intent(user_message),
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {str(e)}")

    # ── 7. Persist conversation history (without system prompt) ───────────
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    update_session(session_id, history)

    # ── 8. Return full response ────────────────────────────────────────────
    return ChatResponse(
        reply=reply,
        intent=intent,
        session_id=session_id,
        trust_score=trust_score,
        confidence_score=None,      # Rohit's RAG fills this later
        mode=mode,
        events=events,
    )