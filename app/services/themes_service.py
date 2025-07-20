from app.models import CreateThemeRequest, DeleteThemeRequest, GetThemesResponse, ApplyThemeRequest, THEME_CAPABLE_DEVICES, DeviceConfig, PowerState, DeviceType
from app.utils.redis_client import redis_client, Namespace
import asyncio
from app.services import device_service
from app.utils import led_strip_util

def save_theme(req: CreateThemeRequest) -> GetThemesResponse:
    redis_client.set(Namespace.THEME, req.name, req.colors)
    return get_all_themes()

def delete_theme(req: DeleteThemeRequest) -> GetThemesResponse:
    redis_client.delete(Namespace.THEME, req.name)
    return get_all_themes()

def get_all_themes() -> GetThemesResponse:
    themes = redis_client.get_all(Namespace.THEME)
    return GetThemesResponse(themes=themes)

async def set_theme(req: ApplyThemeRequest):
    devices = device_service.read_all_devices()

    async def _apply_theme(device: DeviceConfig) -> tuple[DeviceConfig, PowerState]:
        match device.type:
            case DeviceType.LED_STRIP:
                new_state = await led_strip_util.set_led_theme(device, req.colors)
            case _:
                new_state = device.power_state
        return device, new_state

    theme_devices = [device for device in devices if device.type in THEME_CAPABLE_DEVICES]
    results = await asyncio.gather(*[_apply_theme(device) for device in theme_devices])

    for device, new_state in results:
        device.power_state = new_state

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, devices, "name")
    return devices
