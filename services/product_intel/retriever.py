"""ChromaDB retriever for the product_intel collection.

Returns top-k results with full metadata, async-compatible via asyncio.to_thread.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import chromadb

CHROMA_DB_PATH = Path(__file__).resolve().parents[2] / "db" / "chroma"
COLLECTION_NAME = "product_intel"
DEFAULT_TOP_K = 5

_client: chromadb.PersistentClient | None = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
        _collection = _client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def _sync_retrieve(query: str, k: int) -> list[dict[str, Any]]:
    collection = _get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=min(k, collection.count() or 1),
        include=["documents", "metadatas", "distances"],
    )
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted = []
    for doc, meta, dist in zip(docs, metas, distances):
        score = round(1.0 - dist, 4) if dist is not None else 0.0
        formatted.append({
            "page_content": doc,
            "metadata": {**meta},
            "score": score,
            # Convenience top-level fields for the graph
            "source_type": meta.get("source_type", ""),
            "product_area": meta.get("product_area", ""),
            "severity_or_priority": meta.get("severity") or meta.get("priority") or "",
        })
    return formatted


async def retrieve_product_intel(query: str, k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    """Async wrapper — runs ChromaDB query in a thread to avoid blocking the event loop."""
    return await asyncio.to_thread(_sync_retrieve, query, k)
