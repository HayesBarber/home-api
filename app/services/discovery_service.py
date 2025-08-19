from app.utils.redis_client import redis_client, Namespace
from app.models import DeviceDiscoveryResponse, CheckinRequest, CheckinResponse, DeviceConfig, DeviceType, InterfaceDevice
from app.utils import kasa_util, lifx_util, esp_util
from app.services import device_service, themes_service

def checkin_device(req: CheckinRequest) -> CheckinResponse | None:
    if req.type == DeviceType.INTERFACE:
        interface_device = InterfaceDevice(
            name=req.name,
            ip=req.ip,
            mac=req.mac,
        )
        redis_client.set_model(Namespace.INTERFACE_DEVICES, interface_device.name, interface_device)
    else:
        device_config = DeviceConfig(
            name=req.name,
            ip=req.ip,
            mac=req.mac,
            type=req.type,
            power_state=req.power_state,
            room=req.room
        )
        redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

    if not req.return_response:
        return None
    
    return build_checkin_response()

def build_checkin_response() -> CheckinResponse:
    devices = device_service.read_all_devices().devices
    devices_names = [d.name for d in devices]

    themes = themes_service.get_all_themes().themes
    theme_names = []
    theme_colors = []

    for name, colors in themes.items():
        theme_names.append(name)
        theme_colors.append(colors)
    
    epoch_time_seconds = ""
    extras = []
    
    return CheckinResponse(
        device_names=devices_names,
        theme_names=theme_names,
        theme_colors=theme_colors,
        epoch_time_seconds=epoch_time_seconds,
        extras=extras,
    )

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
