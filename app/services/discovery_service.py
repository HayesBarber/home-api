from app.utils.redis_client import redis_client, Namespace
from datetime import datetime, timedelta
from typing import List
from app.models.device import DeviceConfig
from app.utils import kasa_util, lifx_util
from app.utils.logger import LOGGER
from app.services import device_service

def discover_lifx() -> List[DeviceConfig]:
    lifx_devices = lifx_util.discover_lifx_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, lifx_devices, "name")
    return lifx_devices

async def discover_kasa() -> List[DeviceConfig]:
    kasa_devices = await kasa_util.discover_kasa_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, kasa_devices, "name")
    return kasa_devices
