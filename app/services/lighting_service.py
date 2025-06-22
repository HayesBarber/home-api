from app.models.device import DeviceConfig, PowerAction, DeviceType
from app.utils import kasa_util
from app.services import device_config_service

def set_state(name: str, action: PowerAction):
    device = device_config_service.get_device_config(name)
    if not device:
        return
    if device.type == DeviceType.KASA:
        kasa_util.control_kasa_device(device, action)
