from pydantic import BaseModel
from typing import List, Optional
from ipaddress import IPv4Address
from app.models import DeviceType, PowerState
from app.config import settings

class CheckinRequest(BaseModel):
    name: str
    ip: IPv4Address 
    mac: str
    type: DeviceType
    power_state: Optional[PowerState]
    room: str = settings.default_room
    return_response: bool = False

class CheckinResponse(BaseModel):
    device_names: List[str]
    theme_names: List[str]
    theme_colors: List[str]
    epoch_time: str
    current_date: str
