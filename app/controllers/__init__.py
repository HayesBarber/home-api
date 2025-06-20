from fastapi import APIRouter
from app.controllers.discovery_controller import router as discovery_controller

api_router = APIRouter()
api_router.include_router(discovery_controller)
