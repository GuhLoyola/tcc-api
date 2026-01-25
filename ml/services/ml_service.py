from fastapi import HTTPException
from ml.model.model_manager_loader import model_manager
from ml.models.prediction import Prediction
from sqlalchemy.orm import Session
from ml.schemas.ml import PredictionSchema
from ml.utils.ml_utils import is_valid_url, extract_features, check_url_status

load_model = model_manager

def get_predictions(db: Session):
    return db.query(Prediction).all()

def get_predictions_count(db: Session):
    return db.query(Prediction).count()

def make_prediction(url: str, db: Session):
    is_url = url.strip()
    
    if not is_valid_url(is_url):
        raise HTTPException(status_code=400, detail="URL inválida.")
    
    features = extract_features(url)
    url_status = check_url_status(url)
    
    prob_dict = {}
    result_label = None
    confidence = None
    
    model = load_model.model
    encoder = load_model.encoder
    
    if model is None or encoder is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhum modelo treinado disponível. Por favor, use a rota de treinamento antes de fazer previsões."
        )
    
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features)[0]
        prob_dict = dict(zip(encoder.classes_, map(float, probs)))

        phishing_related = ["phishing", "malware", "defacement"]
        phishing_confidence = sum(prob_dict.get(cls, 0.0) for cls in phishing_related)

        top_class = max(prob_dict, key=prob_dict.get)
        confidence = float(prob_dict[top_class])

        if phishing_confidence > prob_dict.get("benign", 0.0):
            result_label = "phishing"
            confidence = phishing_confidence
        else:
            result_label = "benign"
            confidence = prob_dict.get("benign", 0.0)
    
    else:
        pred_label_encoded = model.predict(features)[0]
        pred_label = encoder.inverse_transform([pred_label_encoded])[0]

        if pred_label in {"malware", "defacement"}:
            result_label = "phishing"
        else:
            result_label = pred_label

        prob_dict = {cls: None for cls in encoder.classes_}
        confidence = None

    prob_dict['url_status_code'] = url_status

    new_prediction = Prediction(input_text=url, result=result_label)
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    return PredictionSchema(
        url=url,
        prediction=result_label,
        confidence=confidence,
        probabilities=prob_dict,   
        prediction_id=new_prediction.id
    )    