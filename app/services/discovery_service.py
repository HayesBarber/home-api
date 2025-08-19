from app.utils.redis_client import redis_client, Namespace
from app.models import DeviceDiscoveryResponse, CheckinRequest, CheckinResponse, DeviceConfig, DeviceType
from app.utils import kasa_util, lifx_util, esp_util
from app.services import device_service

def checkin_device(req: CheckinRequest) -> CheckinResponse | None:
    if req.type == DeviceType.INTERFACE:
        pass
    else:
        device_config = DeviceConfig(
            name=req.name,
            ip=req.ip,
            mac=req.mac,
            type=req.type,
            power_state=req.power_state,
            room=req.room
        )
        device_service.upsert_device(device_config)

    if not req.return_response:
        return None
    
    return None

async def discover_lifx() -> DeviceDiscoveryResponse:
    lifx_devices = await lifx_util.discover_lifx_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, lifx_devices, "name")
    return DeviceDiscoveryResponse(
        devices=lifx_devices
    )

async def discover_kasa() -> DeviceDiscoveryResponse:
    kasa_devices = await kasa_util.discover_kasa_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, kasa_devices, "name")
    return DeviceDiscoveryResponse(
        devices=kasa_devices
    )

async def discover_esp(passcode: str, port: int) -> None:
    await esp_util.discover_esp_devices(passcode, port)
