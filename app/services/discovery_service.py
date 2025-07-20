from app.utils.redis_client import redis_client, Namespace
from typing import List
from app.models import DeviceConfig
from app.utils import kasa_util, lifx_util, esp_util

async def discover_lifx() -> List[DeviceConfig]:
    lifx_devices = await lifx_util.discover_lifx_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, lifx_devices, "name")
    return lifx_devices

async def discover_kasa() -> List[DeviceConfig]:
    kasa_devices = await kasa_util.discover_kasa_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, kasa_devices, "name")
    return kasa_devices

async def discover_esp(passcode: str, port: int) -> str:
    await esp_util.discover_esp_devices(passcode, port)
    return "Broadcast sent"
