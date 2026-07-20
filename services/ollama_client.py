# services/ollama_client.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:latest")


async def chat_with_ollama(messages: list[dict]) -> str:
    """
    Send a conversation history to Ollama and get a response.
    `messages` is a list of {"role": "user"/"assistant", "content": "..."} dicts.
    Includes fallback error handling if Ollama is unresponsive.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "No response generated.")
    except Exception as e:
        print(f"[Ollama Error] {type(e).__name__}: {e}")
        return (
            f"Note: Ollama model '{OLLAMA_MODEL}' was unreachable or timed out ({type(e).__name__}). "
            "Please ensure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull gemma3:latest`)."
        )


async def classify_intent(user_message: str) -> str:
    """
    Ask Ollama to classify a user message as SALES, SUPPORT, CARE, or PRODUCT_INTEL.
    Returns exactly one of those four labels (uppercased, stripped).
    Includes pre-checks to route product catalog queries (e.g. details/price of NovaBuds, NovaBook) to SALES.
    """
    msg_lower = user_message.lower()

    # Pre-check: Explicit B2B Product Intelligence queries (Jira tickets, customer feedback, pain points, competitor insights)
    is_product_intel = any(k in msg_lower for k in [
        "jira", "ticket", "customer feedback", "support case", "pain point", "prioritize",
        "prioritization", "roadmap", "competitor", "q3", "feature gap", "usage analytics",
        "revenue impact", "at risk", "latam", "apac", "freshdesk", "salesforce",
        "what should we build", "feedback analysis", "customer signals", "jira tickets"
    ])

    # Pre-check: ShopNova B2C Store Catalog Inquiries (e.g. NovaBuds, NovaBook specs/price)
    is_product_catalog_inquiry = any(k in msg_lower for k in [
        "novabuds", "novabook", "novasound", "shopnova", "earbuds", "headphones",
        "store policy", "return policy", "warranty for", "available colors"
    ]) and not is_product_intel

    if is_product_intel:
        return "PRODUCT_INTEL"

    if is_product_catalog_inquiry:
        return "SALES"

    classification_prompt = (
        "You are an intent classifier for a customer service and product intelligence chatbot.\n"
        "Classify the following user message into exactly one of these categories:\n"
        "- SALES: product inquiries, buying, pricing, specifications, product details, stock, plans, upgrades, discounts\n"
        "- SUPPORT: technical issues, bugs, errors, how-to questions, troubleshooting\n"
        "- CARE: complaints, frustration, refunds, cancellations, account issues, emotional distress\n"
        "- PRODUCT_INTEL: B2B product manager questions about customer pain points, feature prioritization, Q3 roadmap, "
        "competitor analysis, customer feedback signals, 'which features should we build', usage analytics\n\n"
        "CRITICAL: Any question asking about product features, details, price, or specifications of ShopNova products "
        "(e.g. NovaBuds, NovaBook, NovaSound) MUST be classified as SALES, NOT PRODUCT_INTEL.\n\n"
        "Reply with ONLY the category label - no explanation, no punctuation, nothing else.\n\n"
        f"User message: {user_message}"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": classification_prompt}],
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            raw_label = data.get("message", {}).get("content", "").strip().upper()

        for label in ["SALES", "SUPPORT", "CARE", "PRODUCT_INTEL"]:
            if label in raw_label:
                # Double-check guard
                if label == "PRODUCT_INTEL" and is_product_catalog_inquiry:
                    return "SALES"
                return label
    except Exception as e:
        print(f"[Ollama Intent Classifier Warning] {type(e).__name__}: {e}")

    # Safe fallback if Ollama is slow/unavailable
    if is_product_intel:
        return "PRODUCT_INTEL"
    return "SALES" if is_product_catalog_inquiry else "SUPPORT"
