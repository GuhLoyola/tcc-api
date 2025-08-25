from db.models import Prediction
from sqlalchemy.orm import Session

class PredictionService:
    
    @staticmethod
    def list_predictions(db: Session):
        return db.query(Prediction).all()

prediction_service = PredictionService()