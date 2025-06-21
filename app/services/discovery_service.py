from app.utils.redis_client import redis_client, Namespace
from datetime import datetime, timedelta
from typing import List
from app.models.device import DeviceConfig
from app.utils import kasa, lifx

def upsert_device(device_config: DeviceConfig):
    redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

def trigger_discovery():
    lifx_devices = lifx.discover_lifx_devices()
    kasa_devices = kasa.discover_kasa_devices()
    all_devices = lifx_devices + kasa_devices

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, all_devices, "name")

    return {
        "lifx_devices": lifx_devices,
        "kasa_devices": kasa_devices,
    }

def read_all_devices():
    all_configs_dict = redis_client.get_all_models(Namespace.DEVICE_CONFIG, DeviceConfig)
    return list(all_configs_dict.values())

def delete_devcie(name: str):
    redis_client.delete(Namespace.DEVICE_CONFIG, name)

def check_for_offline_devices():
    devices = read_all_devices()
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
