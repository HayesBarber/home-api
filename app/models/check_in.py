from pydantic import BaseModel, model_validator, field_validator
from typing import List, Optional
from ipaddress import IPv4Address
from app.models import DeviceType, PowerState
from app.config import settings

class CheckinRequest(BaseModel):
    name: str
    ip: IPv4Address 
    mac: str
    type: DeviceType
    power_state: Optional[PowerState] = None
    room: str = settings.default_room
    return_response: bool = False

    @field_validator("return_response", mode="before")
    @classmethod
    def parse_return_response(cls, v):
        if isinstance(v, str):
            if v.lower() in {"true", "1", "yes"}:
                return True
            if v.lower() in {"false", "0", "no"}:
                return False
        return v

    @model_validator(mode="after")
    def validate_power_state(self):
        if self.type != DeviceType.INTERFACE and self.power_state is None:
                raise ValueError("power_state is required unless device type is 'interface'")
        return self

class CheckinResponse(BaseModel):
    device_names: List[str]
    theme_names: List[str]
    theme_colors: List[str]
    epoch_time_seconds: str
    extras: List[str]
