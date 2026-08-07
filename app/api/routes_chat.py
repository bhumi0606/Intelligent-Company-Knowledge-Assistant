
from fastapi import APIRouter, HTTPException, status

from app.models.schemas import ChatRequest, ChatResponse
from app.rag.generate_answer import answer_query

chat_router = APIRouter()

@chat_router.post('/query', response_model=ChatResponse)
async def chat_query(query: ChatRequest):
    try:
        answer = answer_query(query.question)
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Can not answer query: {e}"
        )

    return ChatResponse(
        answer = answer
    )