from app.models.device import PowerAction, DeviceType
from app.utils import kasa_util, lifx_util
from app.services import device_config_service

def set_device_state(name: str, action: PowerAction):
    device = device_config_service.get_device_config(name)

    match device.type:
        case DeviceType.KASA:
            new_state = kasa_util.control_kasa_device(device, action)
        case DeviceType.LIFX:
            new_state = lifx_util.control_lifx_device(device, action)
        case _:
            new_state = device.power_state

    device.power_state = new_state
    device_config_service.upsert_device(device)
    return device
