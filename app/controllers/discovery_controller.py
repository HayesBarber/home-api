from fastapi import APIRouter, Response, status
from app.services import discovery_service
from app.models import DeviceDiscoveryResponse, CheckinRequest, CheckinResponse

router = APIRouter(prefix="/discovery", tags=["Discovery"])

@router.post(
    "/check-in",
    responses={
        200: {"model": CheckinResponse},
        204: {"description": "No Content"},
    },
)
def check_in_device(req: CheckinRequest):
    response = discovery_service.checkin_device(req)
    if response:
        return response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/discover/kasa", response_model=DeviceDiscoveryResponse)
async def discover_kasa():
    return await discovery_service.discover_kasa()

@router.post("/discover/lifx", response_model=DeviceDiscoveryResponse)
async def discover_lifx():
    return await discovery_service.discover_lifx()

@router.post("/discover/esp", status_code=DeviceDiscoveryResponse)
async def discover_esp(passcode: str, port: int):
    return await discovery_service.discover_esp(passcode, port)
