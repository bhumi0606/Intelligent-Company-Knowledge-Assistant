
from fastapi import APIRouter, HTTPException, status

from app.agents.router import route
from app.models.schemas import ChatRequest, ChatResponse

chat_router = APIRouter()

@chat_router.post('/query', response_model=ChatResponse)
async def chat_query(query: ChatRequest):
    try:
        answer = route(query.question)
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Can not answer query: {e}"
        )

    return answer