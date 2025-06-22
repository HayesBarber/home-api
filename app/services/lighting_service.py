from app.models.device import PowerAction, DeviceType
from app.utils import kasa_util, redis_client
from app.services import device_config_service

def set_state(name: str, action: PowerAction):
    device = device_config_service.get_device_config(name)
    if not device:
        return
    if device.type == DeviceType.KASA:
        new_state = kasa_util.control_kasa_device(device, action)
        device.power_state = new_state

    device_config_service.upsert_device(device)
    return device
