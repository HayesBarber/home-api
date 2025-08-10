from typing import Optional
from app.services.device_service import get_devices_of_room

def get_room_from_string(name: str) -> Optional[str]:
    devices = get_devices_of_room(name)
    if devices:
        return name
    return None
