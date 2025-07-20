import asyncio
from app.models import PowerAction, DeviceType, Room, DeviceConfig, PowerState, get_room_from_string
from app.utils import kasa_util, lifx_util, led_strip_util
from app.utils.redis_client import redis_client, Namespace
from app.utils.logger import LOGGER
from app.services import device_service
from typing import List, Optional

async def set_state(name: str, action: PowerAction):
    if name == "home":
        return await set_home_state(action)

    room = get_room_from_string(name)
    if room:
        return await set_room_state(room, action)
    
    return await set_device_state(name, action)


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

    return await _perform_power_action([device], action)

async def set_room_state(room: Room, action: PowerAction):
    devices = device_service.get_devices_of_room(room)

    if action == PowerAction.TOGGLE:
        action = PowerAction.ON if get_power_state_of_room(room, devices) == PowerState.OFF else PowerAction.OFF

    return await _perform_power_action(devices, action)

async def set_home_state(action: PowerAction):
    devices = device_service.read_all_devices()

    if action == PowerAction.TOGGLE:
        action = PowerAction.ON if get_power_state_of_home(devices) == PowerState.OFF else PowerAction.OFF

    return await _perform_power_action(devices, action)

async def _perform_power_action(devices: List[DeviceConfig], action: PowerAction):
    new_states = await asyncio.gather(*[
        _get_new_device_state(device, action) for device in devices
    ])

    for device, new_state in zip(devices, new_states):
        device.power_state = new_state

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, devices, "name")
    return devices

async def _get_new_device_state(device: DeviceConfig, action: PowerAction) -> PowerState:
    try:
        match device.type:
            case DeviceType.KASA:
                return await kasa_util.control_kasa_device(device, action)
            case DeviceType.LIFX:
                return await lifx_util.control_lifx_device(device, action)
            case DeviceType.LED_STRIP:
                return await led_strip_util.control_led_strip(device, action)
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
