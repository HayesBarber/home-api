import asyncio
from lifxlan import LifxLAN, Light
from app.models import ControllableDevice, DeviceType, PowerState, PowerAction
from typing import List
from app.services import device_service
from app.utils.logger import LOGGER

_lifx = LifxLAN()

async def discover_lifx_devices() -> List[ControllableDevice]:
    LOGGER.info("Discovering Lifx devices...")
    devices: List[Light] = await asyncio.to_thread(_lifx.get_lights)
    results = []

    for d in devices:
        LOGGER.info(f"Found {d.get_label()} at {d.get_ip_addr()}")
        room, cleaned_name = device_service.extract_room_name(d.get_label())
        power_state = await asyncio.to_thread(d.get_power)
        results.append(
            ControllableDevice(
                name=cleaned_name,
                ip=d.get_ip_addr(),
                mac=d.get_mac_addr(),
                type=DeviceType.LIFX,
                power_state=PowerState.ON if power_state else PowerState.OFF,
                room=room
            )
        )

    if not devices:
        LOGGER.info("No Lifx devices found")

    return results

def _connect(config: ControllableDevice) -> Light:
    light = Light(config.mac, str(config.ip)) 
    return light

async def control_lifx_device(config: ControllableDevice, action: PowerAction) -> PowerState:
    device = _connect(config)
    match action:
        case PowerAction.ON:
            await asyncio.to_thread(device.set_power, "on")
            return PowerState.ON
        case PowerAction.OFF:
            await asyncio.to_thread(device.set_power, "off")
            return PowerState.OFF
        case PowerAction.TOGGLE:
            current_power = await asyncio.to_thread(device.get_power)
            if current_power:
                await asyncio.to_thread(device.set_power, "off")
                return PowerState.OFF
            else:
                await asyncio.to_thread(device.set_power, "on")
                return PowerState.ON

async def update_lifx_device_name(config: ControllableDevice, new_name: str) -> str:
    device = _connect(config)
    await asyncio.to_thread(device.set_label, new_name)
    return new_name
