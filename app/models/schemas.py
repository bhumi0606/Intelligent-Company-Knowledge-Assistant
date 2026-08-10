
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    agent_used: str = Optional[None]