from fastapi import APIRouter, Response, status
from app.services import discovery_service, device_config_service
from app.models.device import DeviceConfig

router = APIRouter(prefix="/discovery", tags=["Discovery"])

@router.post("/check-in", status_code=status.HTTP_204_NO_CONTENT)
def check_in_device(config: DeviceConfig):
    device_config_service.upsert_device(config)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/discover")
def trigger_discovery():
    return discovery_service.trigger_discovery()

@router.get("/read")
def read_all_devices():
    return device_config_service.read_all_devices()

@router.delete("/{device_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_name: str):
    device_config_service.delete_devcie(device_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/check-offline")
def check_for_offline_devices():
    return {
        "offline_count": discovery_service.check_for_offline_devices()
    }
