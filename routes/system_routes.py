from fastapi import APIRouter
from routes.feedback_routes import router as feedback_router
from routes.model_routes import router as model_router
from routes.prediction_routes import router as prediction_router
from controllers.system_controller import system_controller

router = APIRouter()

@router.get("/status")
def get_status():
    return system_controller.get_status()

router.include_router(feedback_router)
router.include_router(model_router)
router.include_router(prediction_router)