from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controllers.feedback_controller import feedback_controller
from db.deps import get_db
from views.schemas.feedback_schema import FeedbackResponse, FeedbackResponseFull, UpdateFeedbackRequest

router = APIRouter()

@router.get("/feedbacks", response_model=List[FeedbackResponseFull])
def list_feedbacks(db: Session = Depends(get_db)):
    return feedback_controller.list_feedbacks(db)

@router.put("/feedback/{prediction_id}", response_model=FeedbackResponse)
def update_feedback(prediction_id: int, payload: UpdateFeedbackRequest, db: Session = Depends(get_db)):
    return feedback_controller.update_feedback(prediction_id, payload, db)