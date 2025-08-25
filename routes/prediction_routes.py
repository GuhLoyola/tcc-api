from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.prediction_controller import prediction_controller
from db.deps import get_db

router = APIRouter()

@router.get("/predictions")
def list_predictions(db: Session = Depends(get_db)):
    return prediction_controller.list_predictions(db)
