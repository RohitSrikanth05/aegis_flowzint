from services.knowledge_base.retriever import retrieve

results = retrieve(
    "How long does shipping take?"
)

print(results)