import asyncio
from kasa import Discover, Device
from app.models.device import DeviceConfig, DeviceType, PowerState, PowerAction
from typing import List
from app.services import device_config_service

async def _discover_kasa_devices_async() -> List[DeviceConfig]:
    print("Discovering Kasa devices...")
    devices = await Discover.discover()

    results = []
    for addr, dev in devices.items():
        await dev.update()
        print(f"Found {dev.alias} at {addr}")
        room, cleaned_name = device_config_service.extract_room_name(dev.alias)
        results.append(
            DeviceConfig(
                name=cleaned_name,
                ip=addr,
                mac=dev.mac,
                type=DeviceType.KASA,
                power_state=PowerState.ON if dev.is_on else PowerState.OFF,
                room=room
            )
        )

    if not results:
        print("No Kasa devices found")

    return results

def discover_kasa_devices() -> List[DeviceConfig]:
    return asyncio.run(_discover_kasa_devices_async())

async def _connect(config: DeviceConfig) -> Device:
    device = await Device.connect(host=str(config.ip))
    return device

async def _control_kasa_device_async(config: DeviceConfig, action: PowerAction) -> PowerState:
    device = await _connect(config)
    match action:
        case PowerAction.ON:
            await device.turn_on()
            return PowerState.ON
        case PowerAction.OFF:
            await device.turn_off()
            return PowerState.OFF
        case PowerAction.TOGGLE:
            if device.is_on:
                await device.turn_off()
                return PowerState.OFF
            else:
                await device.turn_on()
                return PowerState.ON

def control_kasa_device(config: DeviceConfig, action: PowerAction) -> PowerState:
    return asyncio.run(_control_kasa_device_async(config, action))

async def _update_kasa_device_name_async(config: DeviceConfig, new_name: str) -> str:
    device = await _connect(config)
    await device.set_alias(new_name)
    return new_name

def update_kasa_device_name(config: DeviceConfig, new_name: str) -> str:
    return asyncio.run(_update_kasa_device_name_async(config, new_name))

async def _get_kasa_device_power_state(config: DeviceConfig) -> PowerState:
    device = await _connect(config)
    return PowerState.ON if device.is_on else PowerState.OFF

def get_kasa_device_power_state(config: DeviceConfig) -> PowerState:
    return asyncio.run(_get_kasa_device_power_state(config))
