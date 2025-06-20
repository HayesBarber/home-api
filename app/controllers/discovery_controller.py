from fastapi import APIRouter, Response, status
from app.services import discovery_service
from app.models.device import DeviceConfig

router = APIRouter(prefix="/discovery", tags=["Discovery"])

@router.post("/check-in", status_code=status.HTTP_204_NO_CONTENT)
def check_in_device(config: DeviceConfig):
    discovery_service.check_in(config)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/discover")
def trigger_discovery():
    return discovery_service.trigger_discovery()
