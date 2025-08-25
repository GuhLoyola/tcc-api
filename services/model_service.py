from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Model
from views.schemas.model_schema import ModelCreate

class ModelService:
    
    @staticmethod
    def add_model(model: ModelCreate, db: Session):
        if not model.name or not model.version:
            raise HTTPException(status_code=400, detail="Nome e versão do modelo são obrigatórios!")

        existing_model = db.query(Model).filter(
            Model.name == model.name,
            Model.version == model.version
        ).first()
        
        if existing_model:
            raise HTTPException(status_code=400, detail="Modelo já existe no banco de dados")

        existing_active_model = db.query(Model).filter(Model.is_active == True).first()

        new_model = Model(
            name=model.name,
            version=model.version,
            is_active=True if not existing_active_model else False
        )

        db.add(new_model)
        db.commit()
        db.refresh(new_model)

        return new_model
    
    @staticmethod
    def delete_model(model_id: int, db: Session):
        model = db.query(Model).filter(Model.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")
        
        if model.is_active:
            raise HTTPException(status_code=400, detail="Não é possível deletar um modelo ativo.")

        db.delete(model)
        db.commit()

        return Response(status_code=204)
    
    @staticmethod
    def list_models(db: Session):
        return db.query(Model).all()

    @staticmethod
    def activate_model(model_id: int, db: Session):
        model_to_activate = db.query(Model).filter(Model.id == model_id).first()
        
        if not model_to_activate:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")
        
        if model_to_activate.is_active:
            raise HTTPException(status_code=400, detail="Este modelo já está ativo")

        try:
            db.query(Model).filter(Model.is_active == True).update({"is_active": False})
            model_to_activate.is_active = True
            db.commit()
        except IntegrityError:
            raise HTTPException(status_code=500, detail="Erro ao atualizar o modelo ativo")
            
        return {
            "Message": f"Modelo '{model_to_activate.name}' agora está ativo.",
            "Model": {
                "id": model_to_activate.id,
                "name": model_to_activate.name,
                "version": model_to_activate.version
            }
        }

model_service = ModelService()