# services/knowledge_base/pipeline.py
from services.knowledge_base.retriever import retrieve
from services.knowledge_base.confidence import score_retrieval
from services.knowledge_base.gap_logger import log_gap


async def process_query(query):
    chunks = await retrieve(query)

    confidence = await score_retrieval(query, chunks)

    needs_learning = confidence < 5

    learning_item = None

    if needs_learning:
        learning_item = await log_gap(
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