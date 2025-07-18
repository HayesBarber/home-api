from fastapi import APIRouter, Response, status
from app.services import device_service

router = APIRouter(prefix="/device", tags=["Device"])

@router.get("/read")
def read_all_devices():
    return device_service.read_all_devices()

@router.delete("/{device_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_name: str):
    device_service.delete_devcie(device_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/update-name")
async def update_device_name(old_name: str, new_name: str):
    return device_service.update_device_name(old_name, new_name)
