from app.models.device import PowerAction, DeviceType, Room, DeviceConfig, PowerState, get_room_from_string
from app.utils import kasa_util, lifx_util
from app.utils.redis_client import redis_client, Namespace
from app.services import device_config_service
from typing import List, Optional

def set_state(name: str, action: PowerAction):
    if name == "home":
        return set_home_state(action)

    room = get_room_from_string(name)
    if room:
        return set_room_state(room, action)
    
    return set_device_state(name, action)

def _get_new_device_state(device: DeviceConfig, action: PowerAction) -> PowerState:
    match device.type:
        case DeviceType.KASA:
            return kasa_util.control_kasa_device(device, action)
        case DeviceType.LIFX:
            return lifx_util.control_lifx_device(device, action)
        case _:
            return device.power_state

def set_device_state(name: str, action: PowerAction):
    device = device_config_service.get_device_config(name)

    new_state = _get_new_device_state(device, action)

    device.power_state = new_state
    device_config_service.upsert_device(device)
    return device

def set_room_state(room: Room, action: PowerAction):
    devices = device_config_service.get_devices_of_room(room)
    updated_devices = []

    for device in devices:
        new_state = _get_new_device_state(device, action)

        device.power_state = new_state
        updated_devices.append(device)

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, updated_devices, "name")
    return updated_devices

def get_power_state_of_home(devices: Optional[List[DeviceConfig]] = None) -> PowerState:
    if devices is None:
        devices = device_config_service.read_all_devices()
    
    for device in devices:
        match device.type:
            case DeviceType.KASA:
                if kasa_util.get_kasa_device_power_state(device) == PowerState.ON:
                    return PowerState.ON
            case DeviceType.LIFX:
                if lifx_util.get_lifx_device_power_state(device) == PowerState.ON:
                    return PowerState.ON
    
    return PowerState.OFF

def set_home_state(action: PowerAction):
    devices = device_config_service.read_all_devices()
    updated_devices = []

    action = PowerAction.ON if get_power_state_of_home(devices) == PowerState.OFF else PowerAction.OFF

    for device in devices:
        new_state = _get_new_device_state(device, action)

        device.power_state = new_state
        updated_devices.append(device)

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, updated_devices, "name")
    return updated_devices
