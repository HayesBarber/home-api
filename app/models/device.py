from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from typing import Optional, List
from datetime import datetime
from app.models import Room, DeviceType, PowerState

class DeviceConfig(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    type: DeviceType
    power_state: PowerState
    last_updated: Optional[str] = None
    is_offline: bool = False
    room: Optional[Room] = None

    @field_validator("room", mode="before")
    @classmethod
    def set_default_room(cls, v):
        return v or Room.LIVING_ROOM

    @field_validator("last_updated", mode="before")
    @classmethod
    def set_last_updated(cls, v):
        if v is None:
            return datetime.now().isoformat()
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class DeviceReadResponse(BaseModel):
    devices: List[DeviceConfig]

class DeviceDiscoveryResponse(BaseModel):
    devices: List[DeviceConfig]
    
class EffectedDevicesResponse(BaseModel):
    devices: List[DeviceConfig]
