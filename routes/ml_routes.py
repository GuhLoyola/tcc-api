from fastapi import APIRouter, Depends
from schemas.feedback_schema import *
from schemas.prediction_schema import *
from services import ml_service
from db.models import Model, Prediction
from db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/predict", response_model= PredictionResponse, summary="Faz uma previsão com o modelo", description="Recebe um texto e retorna se é verdadeiro ou falso.")
def predict(payload: PredictionRequest, db: Session = Depends(get_db)):
    prediction = ml_service.predict(payload.text)
    
    # Verifica se o modelo já existe no banco de dados, caso contrário, cria um novo registro
    model_record = db.query(Model).filter_by(id=1).first()
    if not model_record:
        model_record = Model(name="TF-IDF", version="1.0")
        db.add(model_record)
        db.commit()
        db.refresh(model_record)
        
    # Cria uma nova previsão no banco de dados
    new_prediction = Prediction(
        input_text=payload.text,
        result=str(prediction),
        model_id=model_record.id
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    return PredictionResponse(text=payload.text, prediction=prediction)
    
@router.post(
    "/feedback", 
    response_model=FeedbackResponse, 
    summary="Enviar feedback sobre uma previsão", 
    description="Permite que o usuário envie um feedback sobre a previsão do modelo."
)
def feedback(feedback: FeedbackRequest):
    print(f"Feedback recebido para {feedback.prediction_id}: {feedback.correct_label}")
    return FeedbackResponse(message="Feedback recebido com sucesso!")