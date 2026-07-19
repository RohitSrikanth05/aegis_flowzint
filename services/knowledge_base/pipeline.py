from services.knowledge_base.retriever import retrieve
from services.knowledge_base.confidence import score_retrieval
from services.knowledge_base.gap_logger import log_gap


def process_query(query: str, query_type: str = None) -> dict:

    # Reject empty or whitespace-only queries immediately
    if not query or not query.strip():
        return {
            "query": query,
            "query_type": query_type,
            "retrieved_chunks": [],
            "confidence": 0,
            "needs_learning": False,
            "learning_item": None,
            "error": "Empty query"
        }

    chunks = retrieve(query)

    confidence = score_retrieval(query, chunks)

    needs_learning = confidence < 5

    learning_item = None

    if needs_learning:
        learning_item = log_gap(
            query,
            chunks,
            confidence,
            query_type
        )

    # Always return chunks — Swathi's engine needs context
    # even on low confidence answers
    return {
        "query": query,
        "query_type": query_type,
        "retrieved_chunks": chunks,
        "confidence": confidence,
        "needs_learning": needs_learning,
        "learning_item": learning_item
    }