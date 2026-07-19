from services.knowledge_base.gap_logger import log_gap
from services.knowledge_base.approval import (
    get_pending_questions,
    approve_question
)

item = log_gap(
    "Do you sell gaming chairs?",
    [],
    2
)

print(item)

queue = get_pending_questions()

print(queue)

if queue:

    print(
        approve_question(
            queue[0]["id"]
        )
    )