# services/ollama_client.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


async def chat_with_ollama(messages: list[dict]) -> str:
    """
    Send a conversation history to Ollama and get a response.
    `messages` is a list of {"role": "user"/"assistant", "content": "..."} dicts.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]


async def classify_intent(user_message: str) -> str:
    """
    Ask Ollama to classify a user message as SALES, SUPPORT, or CARE.
    Returns exactly one of those three labels (uppercased, stripped).
    """
    classification_prompt = (
        "You are an intent classifier for a customer service chatbot.\n"
        "Classify the following user message into exactly one of these categories:\n"
        "- SALES: buying, pricing, plans, upgrades, discounts, product inquiries\n"
        "- SUPPORT: technical issues, bugs, errors, how-to questions, troubleshooting\n"
        "- CARE: complaints, frustration, refunds, cancellations, account issues, emotional distress\n\n"
        "Reply with ONLY the category label — no explanation, no punctuation, nothing else.\n\n"
        f"User message: {user_message}"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": classification_prompt}],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        raw_label = data["message"]["content"].strip().upper()

    # Sanitise — if the model adds extra words, extract just the label
    for label in ["SALES", "SUPPORT", "CARE"]:
        if label in raw_label:
            return label

    return "SUPPORT"  # safe fallback