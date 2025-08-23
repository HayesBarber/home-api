from fastapi import APIRouter
from app.services import weather_service
from app.models import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("", response_model=WeatherResponse)
def get_weather():
    return weather_service.get_current_temperature()
