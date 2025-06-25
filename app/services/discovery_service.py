from app.utils.redis_client import redis_client, Namespace
from datetime import datetime, timedelta
from typing import List
from app.models.device import DeviceConfig
from app.utils import kasa_util, lifx_util
from app.services import device_config_service

def discover_lifx() -> List[DeviceConfig]:
    lifx_devices = lifx_util.discover_lifx_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, lifx_devices, "name")
    return lifx_devices

def discover_kasa() -> List[DeviceConfig]:
    kasa_devices = kasa_util.discover_kasa_devices()
    redis_client.set_all_models(Namespace.DEVICE_CONFIG, kasa_devices, "name")
    return kasa_devices

def trigger_discovery():
    lifx_devices = discover_lifx()
    kasa_devices = discover_kasa()

    return {
        "lifx_devices": lifx_devices,
        "kasa_devices": kasa_devices,
    }

def check_for_offline_devices():
    devices = device_config_service.read_all_devices()
    stale = get_stale_devices(devices)

    for device in stale:
        print(f"{device.name} is stale, marking as offline")
        device.is_offline = True
    
    redis_client.set_all_models(DeviceConfig, stale, "name")
     
    return len(stale)

def get_stale_devices(devices: List[DeviceConfig]) -> List[DeviceConfig]:
    now = datetime.now()
    cutoff = now - timedelta(minutes=15)

    stale_devices = []
    for device in devices:
        if device.last_updated is None:
            continue
        try:
            last_updated_dt = datetime.fromisoformat(device.last_updated)
            if last_updated_dt < cutoff:
                stale_devices.append(device)
        except ValueError:
            continue

    return stale_devices
