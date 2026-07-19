from services.knowledge_base.retriever import retrieve

queries = [
    "How long does shipping take?",
    "Can I cancel my order?",
    "Do you offer EMI?",
    "Which laptop is best for gaming?",
    "Tell me about NovaBook Gaming",
    "Do accessories have warranty?",
    "How do refunds work?"
]

for q in queries:
    print(f"\nQUERY: {q}")
    print("-" * 50)

    results = retrieve(q)

    for r in results[:2]:
        print(r["title"])
        print(r["content"])
        print()