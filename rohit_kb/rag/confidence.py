from rag.llm_provider import generate


def score_retrieval(query, retrieved_chunks):

    context = "\n".join(
        [chunk["content"] for chunk in retrieved_chunks]
    )

    prompt = f"""
User Question:
{query}

Retrieved Context:
{context}

Rate how confident you are that the retrieved context can answer the question.

Return ONLY a number from 1 to 10.

1 = no useful information
10 = perfect answer available
"""

    response = generate(prompt)

    try:
        score = int(
            "".join(
                filter(str.isdigit, response)
            )[:2]
        )

        score = max(
            1,
            min(score, 10)
        )

    except:
        score = 5

    return score