from fastapi import APIRouter
from app.services import weather_service
from app.models import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

