from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.services.auth_service import get_current_user
from core.database import get_db
from ml.schemas.feedback import FeedbackSchema, FeedbackResponse, FeedbackRequest
from ml.schemas.metrics import MetricsSchema
from ml.schemas.ml import PredictionSchema
from ml.services.feedback_service import get_feedbacks, update_feedback
from ml.services.metrics_service import get_metrics
from ml.services.ml_service import get_predictions, get_predictions_count, make_prediction
from user.models.user import User

ml_router = APIRouter(
    prefix='/ml',
    tags=['Machine Learning']
)

@ml_router.post('/prediction', response_model=PredictionSchema)
def prediction_post(url: str, db: Session = Depends(get_db)):
    prediction = make_prediction(url, db)
    return prediction

@ml_router.get('/predictions')
def prediction_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    predictions = get_predictions(db)
    return predictions

@ml_router.get('/predictions/count')
def predictions_count( db: Session = Depends(get_db)):
    predictions = get_predictions_count(db)
    return predictions

@ml_router.get('/metrics', response_model=list[MetricsSchema])
def metric_list(db: Session = Depends(get_db)):
    metrics = get_metrics(db)
    return metrics

@ml_router.get('/feedbacks', response_model=list[FeedbackSchema])
def feedback_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    feedbacks = get_feedbacks(db)
    return feedbacks

@ml_router.put("/feedback/{prediction_id}", response_model=FeedbackResponse)
def make_feedback(prediction_id: int, payload: FeedbackRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    feedback = update_feedback(prediction_id, payload, db)
    return feedback