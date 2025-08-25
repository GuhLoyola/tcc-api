from services.model_service import model_service
from views.schemas.model_schema import ModelCreate
from sqlalchemy.orm import Session

class ModelController:
    
    @staticmethod
    def add_model(model: ModelCreate, db: Session):
        return model_service.add_model(model, db)
    
    @staticmethod
    def delete_model(model_id: int, db: Session):
        return model_service.delete_model(model_id, db)
    
    @staticmethod
    def list_models(db: Session):
        return model_service.list_models(db)
    
    
    @staticmethod
    def activate_model(model_id: int, db: Session):
        return model_service.activate_model(model_id, db)
    
model_controller = ModelController()