"""Top-level async pipeline for product intelligence queries.

Entry point: process_product_query(question) -> dict

Returns:
    {
        "answer": str,
        "route": str,           # pain_points | prioritization | roadmap | competitor | fallback
        "sources": list[dict],  # retrieved evidence metadata
        "priority_table": list[dict] | None,  # only for prioritization route
    }
"""

from __future__ import annotations

from typing import Any

from services.product_intel.retriever import retrieve_product_intel
from services.product_intel.graph import run_graph

DEFAULT_TOP_K = 5


async def process_product_query(question: str, k: int = DEFAULT_TOP_K, username: str = "guest") -> dict[str, Any]:
    """Retrieve relevant product signal documents, then route through the graph."""
    documents = await retrieve_product_intel(question, k=k)

    if not documents:
        return {
            "answer": (
                "I couldn't find relevant product signal data in the knowledge base. "
                "Please make sure the product intelligence data has been seeded and ingested. "
                "Run: python services/product_intel/seed_data.py && python services/product_intel/ingest.py"
            ),
            "route": "fallback",
            "sources": [],
            "priority_table": None,
        }

    result = await run_graph(question, documents, username)
    return result
