# services/knowledge_base/confidence.py
from services.ollama_client import chat_with_ollama


async def score_retrieval(query, retrieved_chunks):

    context = "\n".join(
        [chunk["content"] for chunk in retrieved_chunks]
    )

    if not context.strip():
        return 5

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

    response = await chat_with_ollama(
        [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

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