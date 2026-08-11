
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    question: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    citations: list
    retrieved_chunks: list
    agent_used: str = Optional[None]

class FeedbackRequest(BaseModel):
    session_id: str
    question: str
    retrieved_chunks: list[str]
    final_answer: str
    feedback: str
    timestamp: str