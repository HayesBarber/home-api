from app.utils.redis_client import redis_client, Namespace
from app.utils import kasa_util, lifx_util
from app.models import ControllableDevice, InterfaceDevice, DeviceType, DeviceReadResponse
from app.config import settings
from datetime import datetime

def get_devices_that_checked_in_since_timestamp(timestamp: datetime) -> list[ControllableDevice | InterfaceDevice]:
    result: list[ControllableDevice | InterfaceDevice] = []

    controllables = redis_client.get_all_models(Namespace.CONTROLLABLE_DEVICES, ControllableDevice)
    for device in controllables.values():
        if device.last_updated and device.last_updated > timestamp:
            result.append(device)

    interfaces = redis_client.get_all_models(Namespace.INTERFACE_DEVICES, InterfaceDevice)
    for device in interfaces.values():
        if device.last_updated and device.last_updated > timestamp:
            result.append(device)

    return result

def read_all_devices() -> DeviceReadResponse:
    all_configs_dict = redis_client.get_all_models(Namespace.CONTROLLABLE_DEVICES, ControllableDevice)
    devices = list(all_configs_dict.values())
    return DeviceReadResponse(
        devices=devices
    )

def get_all_rooms() -> set[str]:
    s = set()

    for d in read_all_devices().devices:
        s.add(d.room)
    
    return s

def delete_devcie(name: str):
    redis_client.delete(Namespace.CONTROLLABLE_DEVICES, name)

def get_device_config(name: str) -> ControllableDevice:
    config = redis_client.get_model(Namespace.CONTROLLABLE_DEVICES, name, ControllableDevice)
    if not config:
        raise KeyError(f"{name} config not found")
    return config

def get_devices_of_room(room: str) -> list[ControllableDevice]:
    all_devices = read_all_devices().devices
    return [device for device in all_devices if device.room == room]

async def update_device_name(name: str, new_name: str):
    device = get_device_config(name)

    match device.type:
        case DeviceType.KASA:
            await kasa_util.update_kasa_device_name(device, new_name)
        case DeviceType.LIFX:
            await lifx_util.update_lifx_device_name(device, new_name)
        case _:
            pass

    # deleting since this is changing the primary key
    delete_devcie(name)

def extract_room_name(device_name: str) -> tuple[str, str]:
    first_index = device_name.find("--")
    if first_index != -1:
        second_index = device_name.find("--", first_index + 2)
        if second_index != -1:
            room = device_name[first_index + 2:second_index]
            stripped_name = device_name[second_index + 2:].strip()
            return room, stripped_name
    room = settings.default_room
    stripped_name = device_name.strip()
    return room, stripped_name
