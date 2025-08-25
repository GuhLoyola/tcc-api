from fastapi import HTTPException
from db.models import Feedback
from views.schemas.feedback_schema import UpdateFeedbackRequest, FeedbackResponse
from sqlalchemy.orm import Session

class FeedbackController: 

    @staticmethod
    def list_feedbacks(db: Session):
            return db.query(Feedback).all()

    @staticmethod
    def update_feedback(prediction_id: int, payload: UpdateFeedbackRequest, db: Session):
        feedback = db.query(Feedback).filter_by(prediction_id=prediction_id).first()

        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback não encontrado para essa previsão.")

        feedback.correct_label = payload.correct_label
        db.commit()
        db.refresh(feedback)

        return FeedbackResponse(message="Feedback atualizado com sucesso!")
    
feedback_service = FeedbackController()   