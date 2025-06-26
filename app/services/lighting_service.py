from app.models.device import PowerAction, DeviceType, Room
from app.utils import kasa_util, lifx_util
from app.utils.redis_client import redis_client, Namespace
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

def set_room_state(room: Room, action: PowerAction):
    devices = device_config_service.get_devices_of_room(room)
    updated_devices = []

    for device in devices:
        match device.type:
            case DeviceType.KASA:
                new_state = kasa_util.control_kasa_device(device, action)
            case DeviceType.LIFX:
                new_state = lifx_util.control_lifx_device(device, action)
            case _:
                new_state = device.power_state

        device.power_state = new_state
        updated_devices.append(device)

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, updated_devices, "name")
    return updated_devices

def set_home_state(action: PowerAction):
    devices = device_config_service.read_all_devices()
    updated_devices = []

    for device in devices:
        match device.type:
            case DeviceType.KASA:
                new_state = kasa_util.control_kasa_device(device, action)
            case DeviceType.LIFX:
                new_state = lifx_util.control_lifx_device(device, action)
            case _:
                new_state = device.power_state

        device.power_state = new_state
        updated_devices.append(device)

    redis_client.set_all_models(Namespace.DEVICE_CONFIG, updated_devices, "name")
    return updated_devices
