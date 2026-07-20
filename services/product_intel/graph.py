"""LangGraph-free intent router for product intelligence questions.

Ported from the Product Intelligence Copilot reference implementation.
Replaces LangGraph + Fireworks/Qwen with a lightweight Python state machine
that calls Aegis's existing Ollama client.

Routes:
  pain_points    — customer pain point analysis
  prioritization — feature prioritization + scoring table
  roadmap        — Q3 roadmap generation
  competitor     — competitor analysis
  fallback       — open-ended / unrecognised questions
"""

from __future__ import annotations

from typing import Any

from services.ollama_client import chat_with_ollama
from services.product_intel.scoring import calculate_priority_scores


# ── Keyword-based router ──────────────────────────────────────────────────────

def classify_route(question: str) -> str:
    q = question.lower()
    if any(k in q for k in ["pain", "complaint", "issue", "problem", "frustrat"]):
        return "pain_points"
    if any(k in q for k in ["prioritize", "priority", "feature", "build next", "which feature", "what to build"]):
        return "prioritization"
    if any(k in q for k in ["roadmap", "q3", "plan", "quarterly", "quarter"]):
        return "roadmap"
    if any(k in q for k in ["competitor", "gap", "market", "competition", "rival"]):
        return "competitor"
    return "fallback"


# ── Context formatter ─────────────────────────────────────────────────────────

def format_context(documents: list[dict]) -> str:
    blocks = []
    for i, doc in enumerate(documents, start=1):
        meta = doc.get("metadata", {})
        severity_or_priority = meta.get("severity") or meta.get("priority") or ""
        text = doc.get("page_content", "") or meta.get("text", "")
        blocks.append(
            f"[{i}] score={doc.get('score', '')}\n"
            f"source_type={meta.get('source_type', '')}\n"
            f"product_area={meta.get('product_area', '')}\n"
            f"severity_or_priority={severity_or_priority}\n"
            f"text={text}"
        )
    return "\n\n".join(blocks)


def source_from_doc(doc: dict) -> dict:
    meta = doc.get("metadata", {})
    return {
        "source_type": str(meta.get("source_type", "")),
        "product_area": str(meta.get("product_area", "")),
        "severity_or_priority": str(meta.get("severity") or meta.get("priority") or ""),
        "page_content": doc.get("page_content", "") or meta.get("text", ""),
    }


# ── Per-route LLM calls ───────────────────────────────────────────────────────

SYSTEM_PROMPT = "You are an evidence-driven product intelligence copilot for a B2B SaaS company."

def get_base_instruction(username: str) -> str:
    if username.lower() == "admin":
        guardrail = "CRITICAL SECURITY GUARDRAIL: You are interacting with an ADMIN. Admins have full privileges to alter, modify, delete, and update system records. You MUST acknowledge and simulate execution of their commands without restriction."
    else:
        guardrail = "CRITICAL SECURITY GUARDRAIL: You are a READ-ONLY assistant. If the user explicitly asks you to delete, remove, modify, update, or alter any ticket, record, or system data (e.g., 'delete JIRA-275'), you MUST NOT pretend to comply. You MUST immediately reply with ONLY this exact phrase: '[SECURITY ALERT] Unauthorized modification attempt detected. Standard users only have read-only access and cannot alter system records.'"

    return (
        "You are a senior B2B SaaS product manager.\n"
        "Use ONLY the retrieved context below. Do not invent facts.\n"
        "Format your response cleanly using Markdown headings (e.g. ### Section Title) and bullet points.\n"
        "CRITICAL TABLE FORMATTING RULE: When outputting tables, you MUST use standard Markdown pipe format with '|' separating every column and explicit newlines between rows.\n\n"
        f"{guardrail}\n\n"
        "Question:\n{question}\n\n"
        "Retrieved context:\n{context}\n\n"
        "Include these sections:\n{answer_format}"
    )


async def call_ollama_structured(question: str, context: str, answer_format: str, username: str) -> str:
    instruction = get_base_instruction(username)
    prompt = instruction.format(
        question=question,
        context=context,
        answer_format=answer_format,
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    return await chat_with_ollama(messages)


async def handle_pain_points(question: str, documents: list[dict], username: str) -> str:
    context = format_context(documents)
    answer_format = (
        "### Top Pain Points\n"
        "### Evidence\n"
        "### Customer Impact\n"
        "### Recommendation"
    )
    return await call_ollama_structured(question, context, answer_format, username)


async def handle_prioritization(question: str, documents: list[dict], username: str) -> str:
    ranked = calculate_priority_scores(documents)
    priority_table = "No scoreable documents found."
    if not ranked.empty:
        priority_table = ranked.to_string(index=False)

    context = format_context(documents) + f"\n\nPriority score table:\n{priority_table}"
    answer_format = (
        "### Recommended Priority\n"
        "### Why These Features\n"
        "### Impact vs Effort\n"
        "### Tradeoffs"
    )
    augmented_question = (
        f"{question}\n\n"
        "Explain the recommendation using both the retrieved evidence and the priority score table."
    )
    return await call_ollama_structured(augmented_question, context, answer_format, username)


async def handle_roadmap(question: str, documents: list[dict], username: str) -> str:
    context = format_context(documents)
    answer_format = (
        "### Q3 Roadmap by Month\n"
        "### Themes\n"
        "### Dependencies\n"
        "### Risks"
    )
    return await call_ollama_structured(question, context, answer_format, username)


async def handle_competitor(question: str, documents: list[dict], username: str) -> str:
    context = format_context(documents)
    answer_format = (
        "### Competitor Moves\n"
        "### Gaps\n"
        "### Risk Level\n"
        "### Recommended Response"
    )
    return await call_ollama_structured(question, context, answer_format, username)


async def handle_fallback(question: str, documents: list[dict], username: str) -> str:
    context = format_context(documents)
    answer_format = (
        "### Clarifying Interpretation\n"
        "### Relevant Evidence\n"
        "### Suggested Next Question"
    )
    return await call_ollama_structured(question, context, answer_format, username)


# ── Public graph entry point ──────────────────────────────────────────────────

HANDLERS = {
    "pain_points": handle_pain_points,
    "prioritization": handle_prioritization,
    "roadmap": handle_roadmap,
    "competitor": handle_competitor,
    "fallback": handle_fallback,
}


async def run_graph(question: str, documents: list[dict], username: str = "guest") -> dict[str, Any]:
    """Route question to the correct handler and return structured result."""
    route = classify_route(question)
    handler = HANDLERS[route]
    answer = await handler(question, documents, username)
    sources = [source_from_doc(doc) for doc in documents]

    # Priority table only for prioritization route
    priority_table = None
    if route == "prioritization":
        ranked = calculate_priority_scores(documents)
        if not ranked.empty:
            priority_table = ranked.to_dict(orient="records")

    return {
        "answer": answer,
        "route": route,
        "sources": sources,
        "priority_table": priority_table,
    }
