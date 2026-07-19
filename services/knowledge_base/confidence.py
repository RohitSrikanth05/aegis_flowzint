import re
from difflib import SequenceMatcher


def normalize(text):
    if not text:
        return ""

    return re.sub(
        r"[^a-z0-9\s]",
        "",
        str(text).lower()
    )


def tokenize(text):
    return set(normalize(text).split())


def similarity(a, b):
    return SequenceMatcher(
        None,
        normalize(a),
        normalize(b)
    ).ratio()


def score_retrieval(query, retrieved_chunks):

    if not retrieved_chunks:
        return 0

    query_tokens = tokenize(query)

    best_score = 0

    for chunk in retrieved_chunks:

        # -------------------------------
        # 1. Semantic similarity (60%)
        # -------------------------------
        semantic_score = max(
            0,
            (1 - chunk["distance"]) * 10
        )

        # -------------------------------
        # 2. Title similarity (20%)
        # -------------------------------
        title_similarity = similarity(
            query,
            chunk.get("title", "")
        )

        title_score = title_similarity * 10

        # -------------------------------
        # 3. Keyword overlap (15%)
        # -------------------------------
        keyword_score = 0

        keywords = chunk.get("keywords")

        if keywords:

            keyword_tokens = tokenize(keywords)

            overlap = len(
                query_tokens & keyword_tokens
            )

            if len(keyword_tokens) > 0:

                keyword_score = (
                    overlap /
                    len(keyword_tokens)
                ) * 10

        # -------------------------------
        # 4. Exact title bonus (5%)
        # -------------------------------
        exact_bonus = 0

        if normalize(query) == normalize(
            chunk.get("title", "")
        ):
            exact_bonus = 10

        # -------------------------------
        # Final weighted score
        # -------------------------------
        score = (
            semantic_score * 0.60 +
            title_score * 0.20 +
            keyword_score * 0.15 +
            exact_bonus * 0.05
        )

        best_score = max(
            best_score,
            score
        )

    return round(
        min(best_score, 10)
    )