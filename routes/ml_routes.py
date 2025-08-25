from fastapi import APIRouter, Depends
from controllers.ml_controller import ml_controller
from db.deps import get_db
from services.prediction_service import prediction_service
from views.schemas.prediction_schema import PredictionRequest
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/predict")
def make_prediction(payload: PredictionRequest, db: Session = Depends(get_db)):
    return ml_controller.predict(payload, db)

@router.post("/feedback")
def make_feedback(payload: PredictionRequest, db: Session = Depends(get_db)):
    return ml_controller.feedback(payload, db)