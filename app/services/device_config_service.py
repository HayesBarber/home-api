from app.utils.redis_client import redis_client, Namespace
from app.utils import kasa_util, lifx_util
from app.models.device import DeviceConfig, DeviceType
from typing import Optional

def upsert_device(device_config: DeviceConfig):
    redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

def read_all_devices():
    all_configs_dict = redis_client.get_all_models(Namespace.DEVICE_CONFIG, DeviceConfig)
    return list(all_configs_dict.values())

def delete_devcie(name: str):
    redis_client.delete(Namespace.DEVICE_CONFIG, name)

def get_device_config(name: str) -> Optional[DeviceConfig]:
    return redis_client.get_model(Namespace.DEVICE_CONFIG, name, DeviceConfig)

def update_device_name(name: str, new_name: str):
    device = get_device_config(name)
    if not device:
        return

    match device.type:
        case DeviceType.KASA:
            updated_name = kasa_util.update_kasa_device_name(device, new_name)
        case DeviceType.LIFX:
            updated_name = lifx_util.update_lifx_device_name(device, new_name)
        case DeviceType.LED_STRIP:
            updated_name = device.name

    device.name = updated_name
    upsert_device(device)
    return device
