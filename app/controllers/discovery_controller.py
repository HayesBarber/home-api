from fastapi import APIRouter, Response, status
from app.services import device_service, discovery_service
from app.models.device import DeviceConfig

router = APIRouter(prefix="/discovery", tags=["Discovery"])

@router.post("/check-in", status_code=status.HTTP_204_NO_CONTENT)
def check_in_device(config: DeviceConfig):
    device_service.upsert_device(config)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/discover")
def trigger_discovery():
    return discovery_service.trigger_discovery()

@router.post("/discover/kasa")
def discover_kasa():
    return discovery_service.discover_kasa()

@router.post("/discover/lifx")
def discover_lifx():
    return discovery_service.discover_lifx()

@router.post("/check-offline")
def check_for_offline_devices():
    return {
        "offline_count": discovery_service.check_for_offline_devices()
    }
