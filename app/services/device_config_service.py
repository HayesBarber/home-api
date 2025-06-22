from app.utils.redis_client import redis_client, Namespace
from datetime import datetime, timedelta
from typing import List
from app.models.device import DeviceConfig
from app.utils import kasa_util, lifx_util

def upsert_device(device_config: DeviceConfig):
    redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

def read_all_devices():
    all_configs_dict = redis_client.get_all_models(Namespace.DEVICE_CONFIG, DeviceConfig)
    return list(all_configs_dict.values())

def delete_devcie(name: str):
    redis_client.delete(Namespace.DEVICE_CONFIG, name)
