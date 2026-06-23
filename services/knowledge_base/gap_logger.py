import json
from datetime import datetime

QUEUE_FILE = "services/knowledge_base/learning_queue.json"


def log_gap(
    question,
    retrieved_context,
    confidence
):

    with open(
        QUEUE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        queue = json.load(f)

    # Prevent duplicate questions

    for item in queue:

        if (
            item["question"].lower().strip()
            ==
            question.lower().strip()
        ):

            return {
                "message": "Question already exists",
                "existing_id": item["id"]
            }

    new_item = {
        "id": len(queue) + 1,
        "question": question,
        "retrieved_context": retrieved_context,
        "confidence": confidence,
        "status": "pending",
        "timestamp": str(
            datetime.now()
        )
    }

    queue.append(new_item)

    with open(
        QUEUE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            queue,
            f,
            indent=4
        )

    return new_item