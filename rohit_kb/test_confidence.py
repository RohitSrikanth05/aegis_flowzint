from rag.retriever import retrieve
from rag.confidence import score_retrieval

query = "Do you sell gaming chairs?"

chunks = retrieve(query)

score = score_retrieval(
    query,
    chunks
)

print("Confidence:", score)