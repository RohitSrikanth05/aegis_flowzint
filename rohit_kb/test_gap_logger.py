from rag.retriever import retrieve
from rag.confidence import score_retrieval

from learning.gap_logger import log_gap

query = "Do you sell gaming chairs?"

chunks = retrieve(query)

score = score_retrieval(
    query,
    chunks
)

print(
    "Confidence:",
    score
)

if score < 5:

    item = log_gap(
        query,
        chunks,
        score
    )

    print(
        "Added to learning queue"
    )

    print(item)

else:

    print(
        "No learning needed"
    )