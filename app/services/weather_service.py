import time
from app.config import settings
from app.utils.logger import LOGGER
import openmeteo_requests

_last_fetch_time = 0
_last_temperature = None

def get_current_temperature():
    global _last_fetch_time, _last_temperature
    current_time = time.time()
    if current_time - _last_fetch_time < 600:
        LOGGER.info("Using cached weather response")
        return _last_temperature
    LOGGER.info("Refetching weather data")
    try:
        client = openmeteo_requests.Client()
        params = {
            "latitude": settings.latitude,
            "longitude": settings.longitude,
            "current": "temperature_2m",
            "wind_speed_unit": "mph",
            "temperature_unit": "fahrenheit",
            "precipitation_unit": "inch",
            "timezone": "America/New_York",
        }
        responses = client.weather_api(
            "https://api.open-meteo.com/v1/forecast", params=params
        )
        response = responses[0]
        _last_temperature = response.Current().Variables(0).Value()
        _last_fetch_time = current_time
        return _last_temperature
    except Exception as e:
        LOGGER.error(f"Weather API error: {e}")
        return _last_temperature
