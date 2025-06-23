from fastapi import APIRouter, Response, status
from app.services import device_config_service

router = APIRouter(prefix="/config", tags=["Device Config"])

@router.get("/read")
def read_all_devices():
    return device_config_service.read_all_devices()

@router.delete("/{device_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_name: str):
    device_config_service.delete_devcie(device_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/update-name")
def update_device_name(old_name: str, new_name: str):
    pass
