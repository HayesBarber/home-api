from pydantic import BaseModel
from app.models.device_type import DeviceType
from typing import Dict

class ApplyThemeRequest(BaseModel):
    colors: str

class CreateThemeRequest(BaseModel):
    name: str
    colors: str

class GetThemesResponse(BaseModel):
    themes: Dict[str, str]

class DeleteThemeRequest(BaseModel):
    name: str

THEME_CAPABLE_DEVICES = { DeviceType.LED_STRIP }
