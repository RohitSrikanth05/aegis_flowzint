# routes/admin.py
import asyncio
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional

from utils.database import (
    get_learning_queue_db,
    get_learning_queue_item_db,
    update_learning_queue_status_db,
    reset_all_sessions_db,
    get_all_sessions_summary_db,
)
from services.knowledge_base.retriever import collection
from services.ollama_client import chat_with_ollama

router = APIRouter()


class ResetRequest(BaseModel):
    session_id: Optional[str] = None


# ── GET /sessions & GET /admin/sessions ────────────────────────────────────────

@router.get("/sessions")
@router.get("/admin/sessions")
async def get_admin_sessions_summary():
    """Return overall system trust score summary and all user session trust metrics."""
    return get_all_sessions_summary_db()


# ── GET /learning-queue ──────────────────────────────────────────────────────

@router.get("/learning-queue")
async def get_learning_queue():
    """Return all items in the knowledge gap learning queue."""
    items = get_learning_queue_db()
    return {"items": items, "total": len(items)}


# ── POST /learning-queue/{id}/approve ───────────────────────────────────────

@router.post("/learning-queue/{item_id}/approve")
async def approve_learning_item(item_id: int):
    """
    Approve a knowledge gap item: use LLM to generate an answer, 
    then ingest it into ChromaDB and mark as 'approved'.
    """
    item = get_learning_queue_item_db(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Learning queue item not found")

    if item["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Item is already '{item['status']}', cannot approve again."
        )

    question = item["question"]
    context_chunks = item.get("retrieved_context", [])
    context_text = "\n".join(
        f"[{c.get('title', '')}]: {c.get('content', '')}"
        for c in context_chunks
    )

    # Ask LLM to generate a comprehensive answer
    synthesis_prompt = (
        f"You are a knowledge base curator for ShopNova, an electronics retailer.\n"
        f"A customer asked: \"{question}\"\n\n"
        f"The existing knowledge base had limited information:\n{context_text or 'No relevant context found.'}\n\n"
        f"Write a clear, accurate, and helpful answer that can be added to the knowledge base. "
        f"If there is no available information, write a general helpful response for that category. "
        f"Keep it under 150 words."
    )

    try:
        answer = await chat_with_ollama([{"role": "user", "content": synthesis_prompt}])
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM synthesis failed: {str(e)}")

    # Ingest the new answer into ChromaDB
    doc_id = f"learned_{item_id}"
    try:
        def _ingest():
            # Remove existing doc with this ID if any (idempotent)
            existing = collection.get(ids=[doc_id])
            if existing["ids"]:
                collection.delete(ids=[doc_id])
            collection.add(
                ids=[doc_id],
                documents=[answer],
                metadatas=[{
                    "title": question,
                    "type": "learned_faq",
                    "category": "learned"
                }]
            )

        await asyncio.to_thread(_ingest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChromaDB ingest failed: {str(e)}")

    # Mark as approved in DB
    update_learning_queue_status_db(item_id, "approved")

    return {
        "status": "approved",
        "item_id": item_id,
        "question": question,
        "generated_answer": answer,
        "chroma_doc_id": doc_id,
        "message": "Knowledge gap approved and ingested into ChromaDB."
    }


# ── POST /learning-queue/{id}/reject ────────────────────────────────────────

@router.post("/learning-queue/{item_id}/reject")
async def reject_learning_item(item_id: int):
    """Mark a learning queue item as rejected (will not be ingested)."""
    item = get_learning_queue_item_db(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Learning queue item not found")

    if item["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail=f"Item is already '{item['status']}', cannot reject again."
        )

    update_learning_queue_status_db(item_id, "rejected")
    return {
        "status": "rejected",
        "item_id": item_id,
        "message": "Item has been marked as rejected."
    }


# ── POST /session/reset ──────────────────────────────────────────────────────

@router.post("/session/reset")
async def reset_sessions():
    """
    Reset all sessions, message histories, and trust scores.
    Useful for demo resets.
    """
    reset_all_sessions_db()
    return {
        "status": "ok",
        "message": "All sessions and trust scores have been reset."
    }
