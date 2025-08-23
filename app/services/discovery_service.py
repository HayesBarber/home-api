from app.utils.redis_client import redis_client, Namespace, LOGGER
from app.models import DeviceDiscoveryResponse, CheckinRequest, CheckinResponse, DeviceConfig, DeviceType, InterfaceDevice
from app.utils import kasa_util, lifx_util, esp_util
from app.services import device_service, themes_service, weather_service

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
    
    return build_checkin_response(req)

def _append_room_devices(device_names: list, room: str):
    devices_in_room = device_service.get_devices_of_room(room)
    if len(devices_in_room) > 1:
        device_names.append(room)
    for device in devices_in_room:
        device_names.append(device.name)

def build_checkin_response(req: CheckinRequest) -> CheckinResponse:
    device_names = []
    all_rooms = device_service.get_all_rooms()
    priority_room = req.room if req and req.room in all_rooms else None

    if priority_room:
        _append_room_devices(device_names, priority_room)

    for room in all_rooms:
        if room == priority_room:
            continue
        _append_room_devices(device_names, room)

    device_names.append("Home")

    themes = themes_service.get_all_themes().themes
    theme_names = []
    theme_colors = []
    for name in sorted(themes.keys()):
        theme_names.append(name)
        theme_colors.append(themes[name])

    epoch_time_seconds = LOGGER.epoch_seconds()
    extras = [
        LOGGER.current_date(),
        weather_service.get_current_temperature().temperature
    ]

    return CheckinResponse(
        device_names=device_names,
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
