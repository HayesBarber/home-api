from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from ipaddress import IPv4Address
from typing import List
from app.models import DeviceType, PowerState
from app.config import settings
from app.utils.logger import LOGGER

class InterfaceDevice(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    last_updated: datetime = Field(default_factory=LOGGER.get_now)

class DeviceConfig(InterfaceDevice):
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
