#!/usr/bin/env python3
"""Ingest product intelligence CSVs into a dedicated ChromaDB collection.

Ported from the Product Intelligence Copilot reference implementation.
Adapted to use Aegis's ChromaDB stack instead of Pinecone + Sentence Transformers.

Run after seed_data.py:
    python services/product_intel/ingest.py
"""

from __future__ import annotations

import asyncio
import csv
from pathlib import Path
from typing import Any

import chromadb

RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "product_intel" / "raw"
CHROMA_DB_PATH = Path(__file__).resolve().parents[2] / "db" / "chroma"
COLLECTION_NAME = "product_intel"

PRODUCT_AREA_HINTS = {
    "Dashboard": ["dashboard", "analytics"],
    "Integrations": ["integration", "integrations", "crm", "connector", "marketplace"],
    "Reporting": ["report", "reporting", "export"],
    "AI Assistant": ["ai", "assistant", "copilot", "citation"],
    "Authentication": ["authentication", "sso", "saml", "login"],
    "Billing": ["billing", "invoice", "seat", "plan"],
    "Mobile App": ["mobile", "push"],
    "Notifications": ["notification", "alert", "sla"],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_value(value: Any) -> str:
    return "" if value is None else str(value).strip()


def source_type_from_path(path: Path) -> str:
    return path.stem


def infer_product_area(row: dict) -> str:
    product_area = clean_value(row.get("product_area"))
    if product_area:
        return product_area
    searchable_text = " ".join(clean_value(v).lower() for v in row.values())
    for area, hints in PRODUCT_AREA_HINTS.items():
        if any(hint in searchable_text for hint in hints):
            return area
    return "Unknown"


def row_id(source_type: str, row: dict, index: int) -> str:
    for key in ["id", "ticket_id", "case_id", "account_id"]:
        value = clean_value(row.get(key))
        if value:
            return value
    return f"{source_type}-{index}"


def row_date(row: dict) -> str:
    for key in ["date", "launch_date", "created_at", "source_date"]:
        value = clean_value(row.get(key))
        if value:
            return value
    return ""


def build_metadata(source_type: str, row: dict, index: int) -> dict:
    metadata = {
        "source_type": source_type,
        "product_area": infer_product_area(row),
        "id": row_id(source_type, row, index),
    }
    date_value = row_date(row)
    if date_value:
        metadata["date"] = date_value

    severity = clean_value(row.get("severity"))
    if severity:
        metadata["severity"] = severity

    priority = clean_value(row.get("priority")) or clean_value(row.get("threat_level"))
    if priority:
        metadata["priority"] = priority

    customer_segment = clean_value(row.get("customer_segment"))
    if customer_segment:
        metadata["customer_segment"] = customer_segment

    revenue_impact = clean_value(row.get("revenue_impact"))
    if revenue_impact:
        metadata["revenue_impact"] = revenue_impact

    effort_points = clean_value(row.get("effort_points"))
    if effort_points:
        metadata["effort_points"] = effort_points

    return metadata


# ── Per-source text summarisers ───────────────────────────────────────────────

def summarize_customer_feedback(row: dict) -> str:
    return (
        f"Customer feedback {clean_value(row.get('id'))} from a "
        f"{clean_value(row.get('customer_segment'))} customer in {clean_value(row.get('region'))} "
        f"concerns {clean_value(row.get('product_area'))}. Sentiment is {clean_value(row.get('sentiment'))} "
        f"with {clean_value(row.get('severity'))} severity and {clean_value(row.get('revenue_impact'))} "
        f"revenue impact. Requested feature: {clean_value(row.get('feature_request'))}. "
        f"Description: {clean_value(row.get('description'))}"
    )


def summarize_jira_ticket(row: dict) -> str:
    return (
        f"Jira ticket {clean_value(row.get('ticket_id'))} is a {clean_value(row.get('issue_type'))} "
        f"for {clean_value(row.get('product_area'))}. Priority is {clean_value(row.get('priority'))}, "
        f"status is {clean_value(row.get('status'))}, and estimated effort is "
        f"{clean_value(row.get('effort_points'))} points. Summary: {clean_value(row.get('summary'))}"
    )


def summarize_support_case(row: dict) -> str:
    return (
        f"Support case {clean_value(row.get('case_id'))} affects {clean_value(row.get('product_area'))}. "
        f"Severity is {clean_value(row.get('severity'))}, status is {clean_value(row.get('status'))}, "
        f"and resolution status is {clean_value(row.get('resolution_status'))}. "
        f"Issue: {clean_value(row.get('issue_summary'))}"
    )


def summarize_competitor_insight(row: dict) -> str:
    return (
        f"Competitor insight from {clean_value(row.get('competitor_name'))}: "
        f"they launched or promoted {clean_value(row.get('feature'))} on "
        f"{clean_value(row.get('launch_date'))}. Source type is {clean_value(row.get('source_type'))}. "
        f"Threat level is {clean_value(row.get('threat_level'))}. "
        f"Insight: {clean_value(row.get('insight'))}"
    )


def summarize_usage_analytics(row: dict) -> str:
    return (
        f"Usage analytics for account {clean_value(row.get('account_id'))} in "
        f"{clean_value(row.get('product_area'))}: weekly active users are "
        f"{clean_value(row.get('weekly_active_users'))}, feature adoption rate is "
        f"{clean_value(row.get('feature_adoption_rate'))} percent, churn risk is "
        f"{clean_value(row.get('churn_risk'))}, and NPS score is {clean_value(row.get('nps_score'))}."
    )


SUMMARIZERS = {
    "customer_feedback": summarize_customer_feedback,
    "jira_tickets": summarize_jira_ticket,
    "support_cases": summarize_support_case,
    "competitor_insights": summarize_competitor_insight,
    "usage_analytics": summarize_usage_analytics,
}


def summarize_row(source_type: str, row: dict) -> str:
    summarizer = SUMMARIZERS.get(source_type)
    if summarizer:
        return summarizer(row)
    fields = [f"{k}: {clean_value(v)}" for k, v in row.items() if clean_value(v)]
    return f"{source_type} row with " + "; ".join(fields)


# ── Load documents from CSVs ──────────────────────────────────────────────────

def load_documents(raw_data_dir: Path = RAW_DATA_DIR) -> list[dict]:
    """Return a list of {text, metadata, doc_id} dicts from all CSVs."""
    documents = []
    for csv_path in sorted(raw_data_dir.glob("*.csv")):
        source_type = source_type_from_path(csv_path)
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader, start=1):
                text = summarize_row(source_type, row)
                metadata = build_metadata(source_type, row, index)
                metadata["text"] = text
                doc_id = f"{source_type}-{metadata['id']}"
                documents.append({"id": doc_id, "text": text, "metadata": metadata})
    return documents


# ── Ingest into ChromaDB ──────────────────────────────────────────────────────

def ingest(raw_data_dir: Path = RAW_DATA_DIR) -> None:
    if not raw_data_dir.exists():
        print(f"No data found at {raw_data_dir}. Run seed_data.py first.")
        return

    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))
    # Drop and recreate so re-runs are idempotent
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(COLLECTION_NAME)

    documents = load_documents(raw_data_dir)
    print(f"Loaded {len(documents)} documents from {raw_data_dir}")

    batch_size = 100
    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]
        collection.add(
            ids=[d["id"] for d in batch],
            documents=[d["text"] for d in batch],
            metadatas=[d["metadata"] for d in batch],
        )
        print(f"  Ingested {min(start + batch_size, len(documents))}/{len(documents)} documents")

    print(f"Done. Collection '{COLLECTION_NAME}' has {collection.count()} documents.")


if __name__ == "__main__":
    ingest()
