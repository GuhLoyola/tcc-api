from fastapi import APIRouter, Depends
from db.models import Model
from db.models import Prediction
from schemas.feedback_schema import FeedbackResponse
from schemas.model_schema import ModelSchema
from sqlalchemy.orm import Session
from db.deps import get_db
from pytz import timezone

router = APIRouter()

@router.get("/status", summary="Verifica o status da API")
def get_status():
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "TF-IDF 1.0"
    }
    
@router.post("/add-model", summary="Adiciona um novo modelo")
def add_model(model: ModelSchema, db: Session = Depends(get_db)):

    if not model.name or not model.version:
        return { "Message": "Nome e versão do modelo são obrigatórios!"}
    
    existing_model = db.query(Model).filter(
        Model.name == model.name,
        Model.version == model.version
    ).first()
    
    if existing_model:
        return { "Message": "Não foi possível adicionar, o modelo já existe no banco de dados" }
    
    new_model = Model( name=model.name,version=model.version )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return {
        "Message": "Modelo adicionado com sucesso!",
        "Model": {
            "id": new_model.id,
            "name": new_model.name,
            "version": new_model.version,
            "created_at": new_model.created_at.astimezone(timezone('America/Sao_Paulo')).strftime("%D/%m/%Y - %H:%M:%S")
        }
    }

@router.delete("/delete-model/{model_id}", summary="Deleta um modelo existente")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    
    if not model:
        return { "Message": "Modelo não encontrado!" }
    
    db.delete(model)
    db.commit()
    
    return { "Message": "Modelo deletado com sucesso!" }

@router.get("/models", summary="Lista todos os modelos cadastrados")
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    
    if not models:
        return { "Message": "Nenhum modelo encontrado!" }
    
    return {
        "Message": "Modelos encontrados!",
        "Models": [
            {
                "id": model.id,
                "name": model.name,
                "version": model.version,
                "created_at": model.created_at.astimezone(timezone('America/Sao_Paulo')).strftime("%d/%m/%Y - %H:%M:%S")
            } for model in models
        ]
    }

@router.get("/predictions", summary="Lista o histórico de previsões")
def list_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()

    if not predictions: 
        return { "Message": "Nenhuma previsão encontrada!" }
    
    return {
        "Message": "Previsões encontradas!",
        "Predictions": [
            {
                "id": prediction.id,
                "input_text": prediction.input_text,
                "result": prediction.result,
                "model_id": prediction.model_id,
                "created_at": prediction.created_at.astimezone(timezone('America/Sao_Paulo')).strftime("%d/%m/%Y - %H:%M:%S")
            } for prediction in predictions
        ]
    }

@router.get(
    "/metrics",
    summary="Retorna métricas detalhadas do modelo",
    description="Exibe métricas como acurácia, precisão, recall, F1-score, taxa de falso positivo e falso negativo."
)
def get_metrics():
    try:
        #Por enquanto, retornando métricas fixas como exemplo.
        #Na aplicação real, essas métricas serão calculadas dinamicamente.
        metrics = {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.89,
            "f1_score": 0.90,
            "false_positive_rate": 0.03,
            "false_negative_rate": 0.07,
            "model_version": "TF-IDF 1.0"
        }
        return {
            "Message": "Métricas do modelo encontradas!",
            "Metrics": metrics
        }
    except Exception as e:
        return {
            "Message": "Erro ao buscar métricas do modelo.",
            "Error": str(e)
        }