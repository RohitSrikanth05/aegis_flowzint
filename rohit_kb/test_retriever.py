from rag.retriever import retrieve

results = retrieve(
    "How long does shipping take?"
)

for item in results:
    print(item)
    print("-" * 50)