from fastapi import APIRouter
from app.controllers.discovery_controller import router as discovery_controller
from app.controllers.lighting_controller import router as lighting_controller
from app.controllers.device_controller import router as device_controller
from app.controllers.themes_controller import router as themes_controller
from app.controllers.user_controller import router as users_controller

api_router = APIRouter()
api_router.include_router(discovery_controller)
api_router.include_router(lighting_controller)
api_router.include_router(device_controller)
api_router.include_router(themes_controller)
api_router.include_router(users_controller)
