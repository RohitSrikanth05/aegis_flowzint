from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.knowledge_base.pipeline import process_query
from services.knowledge_base.approval import (
    get_pending_questions,
    approve_question,
    reject_question
)
from services.knowledge_base.gap_logger import get_all_items

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    query_type: str = None  # optional: spec_lookup / policy / complaint / general


class ActionRequest(BaseModel):
    id: str


@router.post("/search")
def search_kb(payload: SearchRequest):

    query = payload.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    result = process_query(query, payload.query_type)
    return result


@router.get("/queue")
def get_full_queue():
    return {
        "items": get_all_items()
    }


@router.get("/queue/pending")
def get_pending():
    items = get_pending_questions()
    return {
        "total": len(items),
        "items": items
    }


@router.post("/approve")
def approve(payload: ActionRequest):

    if not payload.id or not payload.id.strip():
        raise HTTPException(
            status_code=400,
            detail="Item ID cannot be empty"
        )

    result = approve_question(payload.id.strip())

    if result["message"] == "Question not found":
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    if result["message"] == "Item is not pending":
        raise HTTPException(
            status_code=409,
            detail=result["message"]
        )

    return result


@router.post("/reject")
def reject(payload: ActionRequest):

    if not payload.id or not payload.id.strip():
        raise HTTPException(
            status_code=400,
            detail="Item ID cannot be empty"
        )

    result = reject_question(payload.id.strip())

    if result["message"] == "Question not found":
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    if result["message"] == "Item is not pending":
        raise HTTPException(
            status_code=409,
            detail=result["message"]
        )

    return result