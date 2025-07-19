from app.utils.redis_client import redis_client, Namespace
from app.utils import kasa_util, lifx_util
from app.models.device import DeviceConfig, DeviceType, Room
from typing import List

def upsert_device(device_config: DeviceConfig):
    redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

def read_all_devices() -> List[DeviceConfig]:
    all_configs_dict = redis_client.get_all_models(Namespace.DEVICE_CONFIG, DeviceConfig)
    return list(all_configs_dict.values())

def delete_devcie(name: str):
    redis_client.delete(Namespace.DEVICE_CONFIG, name)

def get_device_config(name: str) -> DeviceConfig:
    config = redis_client.get_model(Namespace.DEVICE_CONFIG, name, DeviceConfig)
    if not config:
        raise KeyError(f"{name} config not found")
    return config

def get_devices_of_room(room: Room) -> List[DeviceConfig]:
    all_devices = read_all_devices()
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
    return {"message": "Device will be updated in the system upon next discovery or check-in"}

def extract_room_name(device_name: str) -> tuple[Room, str]:
    if "--bedroom--" in device_name:
        room = Room.BEDROOM
        stripped_name = device_name.replace("--bedroom--", "", 1).strip()
    elif "--living_room--" in device_name:
        room = Room.LIVING_ROOM
        stripped_name = device_name.replace("--living_room--", "", 1).strip()
    elif "--upstairs--" in device_name:
        room = Room.UPSTAIRS
        stripped_name = device_name.replace("--upstairs--", "", 1).strip()
    else:
        room = Room.LIVING_ROOM
        stripped_name = device_name.strip()

    return room, stripped_name
