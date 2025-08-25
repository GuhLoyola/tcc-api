from services.ml_service import ml_service
from views.schemas.feedback_schema import FeedbackRequest, FeedbackResponse
from views.schemas.prediction_schema import PredictionRequest, PredictionResponse
from sqlalchemy.orm import Session

class MlController:
    
    @staticmethod
    def predict(payload: PredictionRequest, db: Session) -> PredictionResponse:
        return ml_service.predict(payload, db)
    
    @staticmethod
    def feedback(payload: FeedbackRequest, db: Session) -> FeedbackResponse:
        return ml_service.feedback(payload, db)
    
ml_controller = MlController()
    