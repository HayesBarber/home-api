from fastapi import APIRouter
from app.controllers.discovery_controller import router as discovery_controller
from app.controllers.lighting_controller import router as lighting_controller
from app.controllers.device_controller import router as device_controller

api_router = APIRouter()
api_router.include_router(discovery_controller)
api_router.include_router(lighting_controller)
api_router.include_router(device_controller)
