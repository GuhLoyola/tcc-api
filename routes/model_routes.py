from typing import List
from fastapi import APIRouter, Depends
from controllers.model_controller import model_controller
from db.deps import get_db
from views.schemas.model_schema import ModelCreate, ModelResponse
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/add-model")
def add_model(model: ModelCreate, db: Session = Depends(get_db)):
    return model_controller.add_model(model, db)

@router.delete("/delete-model/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    return model_controller.delete_model(model_id, db)

@router.get("/models", response_model=List[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    return model_controller.list_models(db)

@router.get("/predictions")
def list_prediction(db: Session = Depends(get_db)):
    return model_controller.list_predictions(db)

@router.post("/models/{model_id}/activate")
def activate_model(model_id: int, db: Session = Depends(get_db)):
    return model_controller.activate_model(model_id, db)