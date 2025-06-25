from fastapi import APIRouter
from app.services import lighting_service
from app.models.device import PowerAction, Room

router = APIRouter(prefix="/lighting", tags=["Lighting"])

@router.post("/set-device-state")
def set_device_state(device_name: str, action: PowerAction):
    return lighting_service.set_device_state(device_name, action)

@router.post("/set-room-state")
def set_room_state(room: Room, action: PowerAction):
    return lighting_service.set_room_state(room, action)
