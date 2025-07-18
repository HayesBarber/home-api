from app.models.device import PowerAction, DeviceType, Room, DeviceConfig, PowerState, get_room_from_string
from app.utils import kasa_util, lifx_util
from app.utils.redis_client import redis_client, Namespace
from app.utils.logger import LOGGER
from app.services import device_service
from typing import List, Optional

async def set_state(name: str, action: PowerAction):
    if name == "home":
        return set_home_state(action)

    room = get_room_from_string(name)
    if room:
        return set_room_state(room, action)
    
    return set_device_state(name, action)

async def _get_new_device_state(device: DeviceConfig, action: PowerAction) -> PowerState:
    try:
        match device.type:
            case DeviceType.KASA:
                return kasa_util.control_kasa_device(device, action)
            case DeviceType.LIFX:
                return lifx_util.control_lifx_device(device, action)
            case _:
                return device.power_state
    except Exception as e:
        LOGGER.error(f"Error setting state for device '{device.name}': {e}")
        return device.power_state

def _get_power_state_of_devices(devices: List[DeviceConfig]) -> PowerState:
    for device in devices:
        if device.power_state == PowerState.ON:
            return PowerState.ON
    
    return PowerState.OFF

def get_power_state_of_room(room: Room, devices: Optional[List[DeviceConfig]] = None) -> PowerState:
    if devices is None:
        devices = device_service.get_devices_of_room(room)

    return _get_power_state_of_devices(devices)

def get_power_state_of_home(devices: Optional[List[DeviceConfig]] = None) -> PowerState:
    if devices is None:
        devices = device_service.read_all_devices()
    
    return _get_power_state_of_devices(devices)

async def set_device_state(name: str, action: PowerAction):
    device = device_service.get_device_config(name)

    return _perform_power_action([device], action)

async def set_room_state(room: Room, action: PowerAction):
    devices = device_service.get_devices_of_room(room)

    if action == PowerAction.TOGGLE:
        action = PowerAction.ON if get_power_state_of_room(room, devices) == PowerState.OFF else PowerAction.OFF

    return _perform_power_action(devices, action)

async def set_home_state(action: PowerAction):
    devices = device_service.read_all_devices()

    if action == PowerAction.TOGGLE:
        action = PowerAction.ON if get_power_state_of_home(devices) == PowerState.OFF else PowerAction.OFF

    return _perform_power_action(devices, action)

async def _perform_power_action(devices: List[DeviceConfig], action: PowerAction):
    updated_devices = []

    for device in devices:
        new_state = await _get_new_device_state(device, action)

        device.power_state = new_state
        updated_devices.append(device)

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, updated_devices, "name")
    return updated_devices
