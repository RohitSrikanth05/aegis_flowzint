from rag.llm_provider import generate

response = generate(
    "Explain what a vector database is in one sentence."
)

print(response)