from pydantic import BaseModel

class WeatherResponse(BaseModel):
    temperature: str
