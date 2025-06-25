from app.utils.redis_client import redis_client, Namespace
from app.utils import kasa_util, lifx_util
from app.models.device import DeviceConfig, DeviceType, Room
from typing import List

def upsert_device(device_config: DeviceConfig):
    redis_client.set_model(Namespace.DEVICE_CONFIG, device_config.name, device_config)

def read_all_devices():
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

def update_device_name(name: str, new_name: str):
    device = get_device_config(name)

    match device.type:
        case DeviceType.KASA:
            updated_name = kasa_util.update_kasa_device_name(device, new_name)
        case DeviceType.LIFX:
            updated_name = lifx_util.update_lifx_device_name(device, new_name)
        case DeviceType.LED_STRIP:
            updated_name = device.name

    device.name = updated_name
    upsert_device(device)
    # deleting since this is changing the primary key
    delete_devcie(name)
    return device

def extract_room_name(device_name: str) -> tuple[Room, str]:
    name_lower = device_name.lower()
    original_name = device_name

    if "bedroom" in name_lower:
        room = Room.BEDROOM
        stripped_name = original_name.replace("bedroom", "").strip()
    elif "living" in name_lower or "living_room" in name_lower:
        room = Room.LIVING_ROOM
        stripped_name = original_name.replace("living room", "").replace("living", "").strip()
    elif "upstairs" in name_lower:
        room = Room.UPSTAIRS
        stripped_name = original_name.replace("upstairs", "").strip()
    else:
        room = Room.LIVING_ROOM
        stripped_name = original_name.strip()

    return room, stripped_name
