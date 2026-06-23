from services.knowledge_base.pipeline import process_query

result = process_query(
    "How long does shipping take?"
)

print(result)