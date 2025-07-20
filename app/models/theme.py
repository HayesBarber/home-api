from pydantic import BaseModel
from app.models.device_type import DeviceType

class Theme(BaseModel):
    colors: str

THEME_CAPABLE_DEVICES = {DeviceType.LED_STRIP}
