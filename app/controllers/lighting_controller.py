from fastapi import APIRouter
from app.services import lighting_service
from app.models.device import DeviceConfig, PowerAction

router = APIRouter(prefix="/lighting", tags=["Lighting"])

@router.post("/set-state")
def set_device_state(device: DeviceConfig, action: PowerAction):
    return lighting_service.set_state(device, action)
