from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.db.models import Feedback
from app.models.schemas import FeedbackRequest
from sqlalchemy.orm import Session

feedback_router = APIRouter()
feedback_values = ["helpful","not_helpful"]

@feedback_router.post('/feedback')
async def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    if request.feedback not in feedback_values:
        raise HTTPException(
            status_code=400,
            detail=f"feedback must be one of {feedback_values}",
        )
 
    try:
        timestamp = datetime.fromisoformat(request.timestamp)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="timestamp must be ISO format",
        )
    
    # store feedback into table
    feedback_row = Feedback(
        session_id=request.session_id,
        question=request.question,
        retrieved_chunks=json.dumps(request.retrieved_chunks),
        final_answer=request.final_answer,
        feedback=request.feedback,
        timestamp=timestamp,
    )
 
    db.add(feedback_row)
    db.commit()
    
    return {"id": feedback_row.id, "status": "feedback added."}