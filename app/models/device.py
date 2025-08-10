from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from typing import Optional, List
from datetime import datetime
from app.models import DeviceType, PowerState
from app.config import settings

class DeviceConfig(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    type: DeviceType
    power_state: PowerState
    last_updated: Optional[str] = None
    is_offline: bool = False
    room: Optional[str] = None

    @field_validator("room", mode="before")
    @classmethod
    def set_default_room(cls, v):
        return v or settings.default_room

    @field_validator("last_updated", mode="before")
    @classmethod
    def set_last_updated(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        if v is None:
            return datetime.now().isoformat()
        return str(v)

class DeviceReadResponse(BaseModel):
    devices: List[DeviceConfig]

class DeviceDiscoveryResponse(BaseModel):
    devices: List[DeviceConfig]

class EffectedDevicesResponse(BaseModel):
    devices: List[DeviceConfig]
