from app.models.device import DeviceConfig, PowerAction, DeviceType
from app.utils import kasa_util

def set_state(device: DeviceConfig, action: PowerAction):
    if device.type == DeviceType.KASA:
        kasa_util.control_kasa_device(device, action)
