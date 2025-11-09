from ml.model.model_manager import ModelManager
from core.config_loader import settings

original_dataset_path = settings.ORIGINAL_DATASET_PATH
dataset_path = settings.DATASET_PATH
model_path = settings.MODEL_PATH
encoder_path = settings.ENCODER_PATH

model_manager = ModelManager(model_path= model_path, encoder_path= encoder_path)