from enum import Enum
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
