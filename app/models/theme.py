from pydantic import BaseModel
from app.models.device_type import DeviceType

class ApplyThemeRequest(BaseModel):
    colors: str

class CreateThemeRequest(BaseModel):
    name: str
    colors: str

class GetThemesResponse(BaseModel):
    themes: dict

class DeleteThemeRequest(BaseModel):
    name: str

THEME_CAPABLE_DEVICES = {DeviceType.LED_STRIP}
