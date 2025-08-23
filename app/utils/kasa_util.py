from kasa import Discover, Device
from app.models import ControllableDevice, DeviceType, PowerState, PowerAction
from typing import List
from app.services import device_service
from app.utils.logger import LOGGER

async def discover_kasa_devices() -> List[ControllableDevice]:
    LOGGER.info("Discovering Kasa devices...")
    devices = await Discover.discover()

    results = []
    for addr, dev in devices.items():
        await dev.update()
        LOGGER.info(f"Found {dev.alias} at {addr}")
        room, cleaned_name = device_service.extract_room_name(dev.alias)
        results.append(
            ControllableDevice(
                name=cleaned_name,
                ip=addr,
                mac=dev.mac,
                type=DeviceType.KASA,
                power_state=PowerState.ON if dev.is_on else PowerState.OFF,
                room=room
            )
        )

    if not results:
        LOGGER.info("No Kasa devices found")

    return results

async def _connect(config: ControllableDevice) -> Device:
    device = await Device.connect(host=str(config.ip))
    return device

async def control_kasa_device(config: ControllableDevice, action: PowerAction) -> PowerState:
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

async def update_kasa_device_name(config: ControllableDevice, new_name: str) -> str:
    device = await _connect(config)
    await device.set_alias(new_name)
    return new_name
