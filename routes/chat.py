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

# Rohit's RAG pipeline
from services.knowledge_base.pipeline import process_query

router = APIRouter()

# One instance per application (they manage state per session_id internally)
detector = TrustDetector()
scorer = TrustScorer()
logger = TrustLogger()
escalation = TrustEscalation()

# ── Intent-specific system prompt addons ─────────────────────────────────────
INTENT_ADDONS = {
    "SALES": (
        "Focus on showcasing ShopNova products, pricing, and upgrade benefits. "
        "Be enthusiastic and helpful about purchases and plans."
    ),
    "SUPPORT": (
        "Focus on resolving technical issues, answering how-to questions, and "
        "providing clear step-by-step guidance."
    ),
    "CARE": (
        "Express empathy and patience. Acknowledge the customer's frustration. "
        "Help with refunds, complaints, and account issues with care."
    ),
}

PROMPT_EXTRACTION_REPLY = (
    "I can’t provide hidden prompts, system instructions, or internal policy details. "
    "If you want, I can still help with the task or question you have."
)


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or "default"
    user_message = request.message
    events = []

    # ── 1. Initialize trust session if first message ──────────────────────
    scorer.initialize_session(session_id)

    # ── 2. Threat detection ───────────────────────────────────────────────
    threats = detector.analyze(user_message)

    # Prompt-extraction attempts are refused before any model call.
    if (
        "prompt_injection" in threats
        or "prompt_extraction" in threats
        or "credential_theft" in threats
    ):
        result = scorer.apply_threat_deduction(session_id, threats)
        logger.log_threat_detection(
            session_id, user_message, threats,
            result["score_before"], result["score_after"]
        )
        events.append("Prompt extraction request blocked")
        events.append(f"Threats detected: {', '.join(threats)}")
        events.append(f"Trust score dropped: {result['score_before']} → {result['score_after']}")
        history = get_session(session_id)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": PROMPT_EXTRACTION_REPLY})
        update_session(session_id, history)

        return ChatResponse(
            reply=PROMPT_EXTRACTION_REPLY,
            intent="UNKNOWN",
            session_id=session_id,
            trust_score=result["score_after"],
            confidence_score=0.0,
            mode=result["mode"],
            events=events,
        )

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

    # ── 4. Run RAG pipeline concurrently with intent classification ───────
    try:
        rag_result, intent = await asyncio.gather(
            process_query(user_message),
            classify_intent(user_message),
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pipeline error: {str(e)}")

    confidence_score = rag_result.get("confidence")
    retrieved_chunks = rag_result.get("retrieved_chunks", [])
    needs_learning = rag_result.get("needs_learning", False)
    learning_item = rag_result.get("learning_item")

    if needs_learning and learning_item:
        events.append(f"Knowledge gap logged for learning: '{user_message[:60]}'")

    if confidence_score is not None:
        events.append(f"RAG confidence: {confidence_score}/10")

    # ── 5. Build context string from RAG chunks ───────────────────────────
    rag_context = ""
    if retrieved_chunks:
        context_lines = []
        for chunk in retrieved_chunks:
            context_lines.append(f"[{chunk.get('title', 'Info')}]: {chunk.get('content', '')}")
        rag_context = "\nRelevant ShopNova Knowledge:\n" + "\n".join(context_lines) + "\n"

    # ── 6. Get mode-specific system prompt with intent + context ──────────
    base_system_prompt = escalation.get_system_prompt(mode)
    intent_addon = INTENT_ADDONS.get(intent, "")
    system_prompt = f"{base_system_prompt}\n\n{intent_addon}\n{rag_context}".strip()

    # ── 7. Build conversation history with system prompt injected ─────────
    history = get_session(session_id)
    messages_with_system = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": user_message}]
    )

    # ── 8. Get LLM reply ──────────────────────────────────────────────────
    try:
        reply = await chat_with_ollama(messages_with_system)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {str(e)}")

    # ── 9. Persist conversation history (without system prompt) ───────────
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    update_session(session_id, history)

    # ── 10. Return full response ──────────────────────────────────────────
    return ChatResponse(
        reply=reply,
        intent=intent,
        session_id=session_id,
        trust_score=trust_score,
        confidence_score=float(confidence_score) if confidence_score is not None else None,
        mode=mode,
        events=events,
    )