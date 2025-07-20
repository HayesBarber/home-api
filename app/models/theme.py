from pydantic import BaseModel
from app.models.device_type import DeviceType

class ApplyThemeRequest(BaseModel):
    colors: str

THEME_CAPABLE_DEVICES = {DeviceType.LED_STRIP}
