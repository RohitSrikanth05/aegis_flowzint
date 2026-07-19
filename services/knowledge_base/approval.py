import os

import chromadb
from dotenv import load_dotenv
from groq import Groq

from services.knowledge_base.gap_logger import (
    get_all_items,
    get_pending_items,
    update_item
)
from services.knowledge_base.paths import DB_PATH

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name="shopnova",
        metadata={"hnsw:space": "cosine"}
    )


def get_pending_questions() -> list:
    return get_pending_items()


def _build_prompt(question: str, context_text: str, query_type: str) -> str:

    if query_type == "spec_lookup":
        return (
            f"A customer asked ShopNova about product specs: \"{question}\"\n\n"
            f"Available context from our knowledge base: {context_text}\n\n"
            "Write a short, factual spec-lookup answer for ShopNova's "
            "electronics store knowledge base. Lead with the concrete "
            "spec/number the customer asked about. Format it exactly as:\n"
            "Q: [question]\n"
            "A: [answer in under 60 words]\n\n"
            "Return only the FAQ text, nothing else."
        )

    if query_type == "policy":
        return (
            f"A customer asked ShopNova about a store policy: \"{question}\"\n\n"
            f"Available context from our knowledge base: {context_text}\n\n"
            "Write a short, precise policy answer for ShopNova's "
            "electronics store knowledge base. State any conditions, "
            "timeframes, or exceptions clearly. Format it exactly as:\n"
            "Q: [question]\n"
            "A: [answer in under 60 words]\n\n"
            "Return only the FAQ text, nothing else."
        )

    if query_type == "complaint":
        return (
            f"A customer complaint/issue was raised with ShopNova: \"{question}\"\n\n"
            f"Available context from our knowledge base: {context_text}\n\n"
            "Write a short, empathetic resolution-focused answer for ShopNova's "
            "electronics store knowledge base. Acknowledge the issue, then give "
            "the concrete next step or resolution. Format it exactly as:\n"
            "Q: [question]\n"
            "A: [answer in under 60 words]\n\n"
            "Return only the FAQ text, nothing else."
        )

    # "general" or unrecognized query_type falls back to the original FAQ template
    return (
        f"A customer asked ShopNova: \"{question}\"\n\n"
        f"Available context from our knowledge base: {context_text}\n\n"
        "Write a short, accurate FAQ answer for ShopNova's "
        "electronics store knowledge base. "
        "Format it exactly as:\n"
        "Q: [question]\n"
        "A: [answer in under 60 words]\n\n"
        "Return only the FAQ text, nothing else."
    )


def _draft_entry(question: str, context: list, query_type: str = None) -> str:

    context_text = " ".join(
        chunk.get("content", "")
        for chunk in context
        if isinstance(chunk, dict)
    )

    prompt = _build_prompt(question, context_text, query_type or "general")

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        max_tokens=150,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def approve_question(item_id: str) -> dict:

    queue = get_all_items()

    for item in queue:

        if item["id"] == item_id:

            if item["status"].lower() not in ["pending", "pending review"]:
                return {
                    "message": "Item is not pending",
                    "id": item_id
                }

            # Use Groq to draft a real KB entry
            print(f"[APPROVAL] Drafting entry for: '{item['question']}'")

            drafted = _draft_entry(
                item["question"],
                item.get("retrieved_context", []),
                item.get("query_type")
            )

            # Add to ChromaDB permanently
            collection = get_collection()
            new_id = f"learned_{item_id[:8]}"

            collection.upsert(
                ids=[new_id],
                documents=[drafted],
                metadatas=[{
                    "title": item["question"],
                    "type": "faq",
                    "category": "learned"
                }]
            )

            # Update queue status
            update_item(item_id, "Approved", drafted)

            print(f"[APPROVAL] Added to ChromaDB: {drafted[:80]}...")

            return {
                "message": "Approved and added to knowledge base",
                "id": item_id,
                "drafted_entry": drafted
            }

    return {
        "message": "Question not found",
        "id": item_id
    }


def reject_question(item_id: str) -> dict:

    queue = get_all_items()

    for item in queue:

        if item["id"] == item_id:

            if item["status"].lower() not in ["pending", "pending review"]:
                return {
                    "message": "Item is not pending",
                    "id": item_id
                }

            update_item(item_id, "Rejected")

            return {
                "message": "Question rejected",
                "id": item_id
            }

    return {
        "message": "Question not found",
        "id": item_id
    }