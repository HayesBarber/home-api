from fastapi import APIRouter
from app.services import lighting_service
from app.models.device import PowerAction

router = APIRouter(prefix="/lighting", tags=["Lighting"])

@router.post("/set-state")
def set_device_state(device_name: str, action: PowerAction):
    return lighting_service.set_state(device_name, action)
