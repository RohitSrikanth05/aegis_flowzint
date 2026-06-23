# services/ollama_client.py
import ollama

MODEL = "llama3.2:3b"

def chat_with_ollama(messages: list[dict]) -> str:
    """
    Send a list of messages to Ollama and get a reply string back.
    messages format: [{"role": "user", "content": "..."}, ...]
    """
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )
    return response["message"]["content"]