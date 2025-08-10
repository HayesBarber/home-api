from enum import Enum
from typing import Optional
from app.services.device_service import get_devices_of_room

class Room(str, Enum):
    BEDROOM = "bedroom"
    LIVING_ROOM = "living_room"
    UPSTAIRS = "upstairs"

def get_room_from_string(name: str) -> Optional[Room]:
    devices = get_devices_of_room(name)
    if devices:
        return name
    return None
