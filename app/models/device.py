from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from ipaddress import IPv4Address
from app.models import DeviceType, PowerState
from app.config import settings
from app.utils.logger import LOGGER


class InterfaceDevice(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    last_updated: datetime = Field(default_factory=LOGGER.get_now)
    esp_flag: bool = False


class ControllableDevice(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    type: DeviceType
    power_state: PowerState
    room: str = settings.default_room
    last_updated: datetime = Field(default_factory=LOGGER.get_now)
    esp_flag: bool = False

    @field_validator("room", mode="before")
    @classmethod
    def set_default_room(cls, v):
        if not v or not str(v).strip():
            return settings.default_room
        return v


class DeviceReadResponse(BaseModel):
    devices: list[ControllableDevice]


class InterfaceDeviceReadResponse(BaseModel):
    devices: list[InterfaceDevice]


class DeviceDiscoveryResponse(BaseModel):
    controllable_devices: list[ControllableDevice] = Field(default_factory=list)
    interface_devices: list[InterfaceDevice] = Field(default_factory=list)


class EffectedDevicesResponse(BaseModel):
    devices: list[ControllableDevice]
