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

@router.get("/read")
def read_all_devices():
    return discovery_service.read_all_devices()

@router.delete("/{device_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_name: str):
    discovery_service.delete_devcie(device_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/check-offline", status_code=status.HTTP_204_NO_CONTENT)
def check_for_offline_devices():
    discovery_service.check_for_offline_devices()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
