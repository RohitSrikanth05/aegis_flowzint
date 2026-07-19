import json
import os
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(BASE_DIR, "learning_queue.json")


def _load_queue() -> list:
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_queue(queue: list):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=4)


def log_gap(question: str, retrieved_context: list, confidence: float, query_type: str = None) -> dict:

    # Reject empty or whitespace-only questions
    if not question or not question.strip():
        return {"message": "Empty question — not logged"}

    queue = _load_queue()

    # Prevent duplicate pending entries
    for item in queue:
        if (
            item["question"].lower().strip()
            == question.lower().strip()
            and item["status"].lower() in ["pending", "pending review"]
        ):
            return {
                "message": "Question already pending",
                "existing_id": item["id"]
            }

    new_item = {
        "id": str(uuid.uuid4()),
        "question": question.strip(),
        "retrieved_context": retrieved_context,
        "confidence": confidence,
        "query_type": query_type or "general",
        "status": "pending review",
        "drafted_entry": None,
        "timestamp": datetime.now().isoformat()
    }

    queue.append(new_item)
    _save_queue(queue)

    print(f"[LEARNING QUEUE] Flagged: '{question}' (confidence: {confidence})")
    return new_item


def get_all_items() -> list:
    return _load_queue()


def get_pending_items() -> list:
    return [
        item for item in _load_queue()
        if item["status"].lower() in ["pending", "pending review"]
    ]


def update_item(item_id: str, status: str, drafted_entry: str = None) -> bool:
    queue = _load_queue()
    for item in queue:
        if item["id"] == item_id:
            item["status"] = status
            if drafted_entry is not None:
                item["drafted_entry"] = drafted_entry
            _save_queue(queue)
            return True
    return False