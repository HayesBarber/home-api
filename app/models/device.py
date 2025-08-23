from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from typing import List
from app.models import DeviceType, PowerState
from app.config import settings

class InterfaceDevice(BaseModel):
    name: str
    ip: IPv4Address
    mac: str

class DeviceConfig(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    type: DeviceType
    power_state: PowerState
    room: str = settings.default_room

    @field_validator("room", mode="before")
    @classmethod
    def set_default_room(cls, v):
        if not v or not str(v).strip():
            return settings.default_room
        return v

class DeviceReadResponse(BaseModel):
    devices: List[DeviceConfig]

class DeviceDiscoveryResponse(BaseModel):
    devices: List[DeviceConfig]

class EffectedDevicesResponse(BaseModel):
    devices: List[DeviceConfig]
