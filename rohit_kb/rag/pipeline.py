from rag.retriever import retrieve
from rag.confidence import score_retrieval

from learning.gap_logger import log_gap


def process_query(query):

    chunks = retrieve(query)

    confidence = score_retrieval(
        query,
        chunks
    )

    needs_learning = (
        confidence < 5
    )

    learning_item = None

    if needs_learning:

        learning_item = log_gap(
            query,
            chunks,
            confidence
        )

    return {
        "query": query,
        "retrieved_chunks": chunks,
        "confidence": confidence,
        "needs_learning": needs_learning,
        "learning_item": learning_item
    }