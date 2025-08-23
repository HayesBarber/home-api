from fastapi import APIRouter
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])

