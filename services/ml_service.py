from core.config import settings
import joblib
import os

def load_model():
    # Carrega o modelo salvo no caminho das configurações
    if not os.path.exists(settings.MODEL_PATH):
        raise FileNotFoundError(f"Modelo não encontrado em {settings.MODEL_PATH}")
    return joblib.load(settings.MODEL_PATH)

def predict(text: str) -> bool:
    # Garante que o texto não está vazio
    if not text or not text.strip():
        raise ValueError("O texto de entrada está vazio.")
    # Carrega o modelo e faz a predição
    model = load_model()
    result = model.predict([text.strip()])
    return