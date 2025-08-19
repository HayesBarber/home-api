from pydantic import BaseModel, model_validator
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
    room: str = Optional[str]
    return_response: bool = False

    @model_validator(mode="after")
    def validate_power_state(self):
        if self.type != DeviceType.INTERFACE :
            if self.power_state is None:
                raise ValueError("power_state is required unless device type is 'interface'")
            if self.room is None:
                raise ValueError("room is required unless device type is 'interface'")
        return self

class CheckinResponse(BaseModel):
    device_names: List[str]
    theme_names: List[str]
    theme_colors: List[str]
    epoch_time_seconds: str
    extras: List[str]
