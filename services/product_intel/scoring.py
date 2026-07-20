"""Multi-factor priority scoring for product areas.

Ported from the Product Intelligence Copilot reference implementation.
Adapted to work with Aegis's ChromaDB document format (dict-based matches).

Scoring formula:
    Final Score = (Frequency × 2) + (Severity × 3) + (Customer Impact × 2)
                  + (Competitor Pressure × 2) - Effort
"""

from __future__ import annotations

import re
from typing import Any

import pandas as pd


FEATURE_AREAS = [
    "Dashboard",
    "Integrations",
    "Reporting",
    "AI Assistant",
    "Authentication",
    "Billing",
    "Mobile App",
    "Notifications",
]

SEVERITY_VALUES = {
    "critical": 5,
    "urgent": 5,
    "p0": 5,
    "high": 4,
    "p1": 4,
    "medium": 2,
    "p2": 2,
    "low": 1,
    "p3": 1,
}

SEGMENT_VALUES = {
    "strategic": 4,
    "enterprise": 4,
    "mid-market": 3,
    "mid market": 3,
    "smb": 2,
    "startup": 1,
}

REVENUE_IMPACT_VALUES = {
    "at risk": 5,
    "high": 4,
    "medium": 2,
    "low": 1,
}

COMPETITOR_THREAT_VALUES = {
    "critical": 5,
    "high": 4,
    "medium": 2,
    "low": 1,
}


def normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def first_present(metadata: dict, keys: list[str]) -> str:
    for key in keys:
        value = metadata.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def value_from_map(value: str, values: dict[str, int]) -> int:
    value_lower = normalized(value)
    for label, score in values.items():
        if label in value_lower:
            return score
    return 0


def severity_score(metadata: dict, text: str) -> int:
    explicit_value = first_present(metadata, ["severity", "priority"])
    explicit_score = value_from_map(explicit_value, SEVERITY_VALUES)
    if explicit_score:
        return explicit_score
    text_lower = normalized(text)
    for label, score in SEVERITY_VALUES.items():
        if re.search(rf"\b{re.escape(label)}\b", text_lower):
            return score
    return 0


def customer_impact_score(metadata: dict, text: str) -> int:
    segment = first_present(metadata, ["customer_segment", "segment"])
    revenue_impact = first_present(metadata, ["revenue_impact"])

    text_lower = normalized(text)
    seg_score = value_from_map(segment, SEGMENT_VALUES)
    if not seg_score:
        seg_score = max(
            (score for label, score in SEGMENT_VALUES.items() if label in text_lower),
            default=0,
        )

    rev_score = value_from_map(revenue_impact, REVENUE_IMPACT_VALUES)
    if not rev_score:
        rev_score = max(
            (score for label, score in REVENUE_IMPACT_VALUES.items()
             if f"{label} revenue impact" in text_lower),
            default=0,
        )

    return seg_score + rev_score


def competitor_pressure_score(metadata: dict, text: str) -> int:
    source_type = normalized(metadata.get("source_type"))
    if "competitor" not in source_type:
        return 0
    threat = first_present(metadata, ["threat_level", "priority", "severity"])
    score = value_from_map(threat, COMPETITOR_THREAT_VALUES)
    if score:
        return score
    text_lower = normalized(text)
    for label, value in COMPETITOR_THREAT_VALUES.items():
        if f"threat level is {label}" in text_lower or f"{label} threat" in text_lower:
            return value
    return 2  # default non-zero for any competitor doc


def effort_score(metadata: dict, text: str) -> int:
    effort = first_present(metadata, ["effort_points", "effort"])
    if effort:
        match = re.search(r"\d+", effort)
        if match:
            return int(match.group(0))
    match = re.search(
        r"(?:effort is|estimated effort is|estimated effort)\s+(\d+)\s+points",
        normalized(text),
    )
    if match:
        return int(match.group(1))
    return 0


def recommendation_for(final_score: int) -> str:
    if final_score >= 35:
        return "Prioritize immediately"
    if final_score >= 20:
        return "Prioritize next"
    if final_score >= 10:
        return "Monitor and validate"
    return "Defer unless strategically required"


def calculate_priority_scores(documents: list[dict]) -> pd.DataFrame:
    """Rank product areas from retrieved ChromaDB documents.

    Each document is a dict with 'page_content', 'metadata', and optional
    top-level convenience fields produced by retriever.py.
    """
    grouped: dict[str, dict[str, int]] = {}

    for doc in documents:
        metadata = doc.get("metadata", {})
        text = doc.get("page_content", "") or metadata.get("text", "")
        product_area = str(metadata.get("product_area") or "").strip()
        if product_area not in FEATURE_AREAS:
            continue

        scores = grouped.setdefault(product_area, {
            "frequency_score": 0,
            "severity_score": 0,
            "customer_impact_score": 0,
            "competitor_pressure_score": 0,
            "effort_score": 0,
        })
        scores["frequency_score"] += 1
        scores["severity_score"] += severity_score(metadata, text)
        scores["customer_impact_score"] += customer_impact_score(metadata, text)
        scores["competitor_pressure_score"] += competitor_pressure_score(metadata, text)
        scores["effort_score"] += effort_score(metadata, text)

    rows = []
    for product_area, scores in grouped.items():
        final = (
            scores["frequency_score"] * 2
            + scores["severity_score"] * 3
            + scores["customer_impact_score"] * 2
            + scores["competitor_pressure_score"] * 2
            - scores["effort_score"]
        )
        rows.append({
            "product_area": product_area,
            **scores,
            "final_score": final,
            "recommendation": recommendation_for(final),
        })

    if not rows:
        return pd.DataFrame(columns=[
            "product_area", "frequency_score", "severity_score",
            "customer_impact_score", "competitor_pressure_score",
            "effort_score", "final_score", "recommendation",
        ])

    return (
        pd.DataFrame(rows)
        .sort_values(
            by=["final_score", "frequency_score", "severity_score"],
            ascending=[False, False, False],
        )
        .reset_index(drop=True)
    )
