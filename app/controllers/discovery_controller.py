from fastapi import APIRouter, Response, status
from app.services import device_service, discovery_service
from app.models import DeviceConfig, DeviceDiscoveryResponse

router = APIRouter(prefix="/discovery", tags=["Discovery"])

@router.post("/check-in", status_code=status.HTTP_204_NO_CONTENT)
def check_in_device(config: DeviceConfig):
    device_service.upsert_device(config)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/discover/kasa", response_model=DeviceDiscoveryResponse)
async def discover_kasa():
    return await discovery_service.discover_kasa()

@router.post("/discover/lifx", response_model=DeviceDiscoveryResponse)
async def discover_lifx():
    return await discovery_service.discover_lifx()

@router.post("/discover/esp", status_code=status.HTTP_204_NO_CONTENT)
async def discover_esp(passcode: str, port: int):
    await discovery_service.discover_esp(passcode, port)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
