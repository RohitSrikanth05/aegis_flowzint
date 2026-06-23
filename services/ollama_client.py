import ollama

MODEL = "llama3.2:3b"

def chat_with_ollama(messages: list[dict]) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response["message"]["content"]