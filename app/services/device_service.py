from app.utils.redis_client import redis_client, Namespace
from app.utils import kasa_util, lifx_util
from app.models import ControllableDevice, DeviceType, DeviceReadResponse
from typing import List
from app.config import settings

def read_all_devices() -> DeviceReadResponse:
    all_configs_dict = redis_client.get_all_models(Namespace.DEVICE_CONFIG, ControllableDevice)
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
    redis_client.delete(Namespace.DEVICE_CONFIG, name)

def get_device_config(name: str) -> ControllableDevice:
    config = redis_client.get_model(Namespace.DEVICE_CONFIG, name, ControllableDevice)
    if not config:
        raise KeyError(f"{name} config not found")
    return config

def get_devices_of_room(room: str) -> List[ControllableDevice]:
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
