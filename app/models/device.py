from enum import Enum
from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
from typing import Optional
from datetime import datetime
from typing import Optional

class Room(str, Enum):
    BEDROOM = "bedroom"
    LIVING_ROOM = "living_room"
    UPSTAIRS = "upstairs"

def get_room_from_string(name: str) -> Optional[Room]:
    for room in Room:
        if room.value == name:
            return room
    return None

class DeviceType(str, Enum):
    KASA = "kasa"
    LIFX = "lifx"
    OTHER = "other"

class PowerState(str, Enum):
    ON = "on"
    OFF = "off"

class PowerAction(str, Enum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"

class DeviceConfig(BaseModel):
    name: str
    ip: IPv4Address
    mac: str
    type: DeviceType
    power_state: PowerState
    last_updated: Optional[str] = None
    is_offline: bool = False
    room: Room = Room.LIVING_ROOM

    @field_validator("last_updated", mode="before")
    @classmethod
    def set_last_updated(cls, v):
        if v is None:
            return datetime.now().isoformat()
        if isinstance(v, datetime):
            return v.isoformat()
        return v
