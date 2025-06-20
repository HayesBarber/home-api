from app.utils.redis_client import redis_client, Namespace
from app.models.device import DeviceConfig
from app.utils import kasa, lifx

def check_in(device_config: DeviceConfig):
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
