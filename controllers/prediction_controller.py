from services.prediction_service import prediction_service
from sqlalchemy.orm import Session

class PredictionController:
    
    @staticmethod
    def list_predictions(db: Session):
        return prediction_service.list_predictions(db)
    
prediction_controller = PredictionController()