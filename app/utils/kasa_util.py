import asyncio
from kasa import Discover, Device
from app.models.device import DeviceConfig, DeviceType, PowerState, PowerAction
from typing import List

async def _discover_kasa_devices_async() -> List[DeviceConfig]:
    print("Discovering Kasa devices...")
    devices = await Discover.discover()

    results = []
    for addr, dev in devices.items():
        await dev.update()
        print(f"Found {dev.alias} at {addr}")
        results.append(
            DeviceConfig(
                name=dev.alias,
                ip=addr,
                type=DeviceType.KASA,
                power_state=PowerState.ON if dev.is_on else PowerState.OFF,
            )
        )

    if not results:
        print("No Kasa devices found")

    return results

def discover_kasa_devices() -> List[DeviceConfig]:
    return asyncio.run(_discover_kasa_devices_async())

async def _control_kasa_device_async(config: DeviceConfig, action: PowerAction):
    device = await Device.connect(host=config.ip)
    match action:
        case PowerAction.ON:
            await device.turn_on()
        case PowerAction.OFF:
            await device.turn_off()
        case PowerAction.TOGGLE:
            await device.turn_off() if device.is_on else await device.turn_on()

def control_kasa_device(config: DeviceConfig, action: PowerAction):
    return asyncio.run(_control_kasa_device_async(config, action))

