from lifxlan import LifxLAN, Light
from app import config
from app.models.device import DeviceConfig, DeviceType, PowerState, PowerAction
from typing import List
from app.services import device_config_service
from app.utils.logger import LOGGER

_lifx = LifxLAN(config.NUM_OF_LIFX_LIGHTS)

def discover_lifx_devices() -> List[DeviceConfig]:
    LOGGER.info("Discovering Lifx devices...")
    devices: List[Light] = _lifx.get_lights()
    results = []

    for d in devices:
        LOGGER.info(f"Found {d.get_label()} at {d.get_ip_addr()}")
        room, cleaned_name = device_config_service.extract_room_name(d.get_label())
        results.append(
            DeviceConfig(
                name=cleaned_name,
                ip=d.get_ip_addr(),
                mac=d.get_mac_addr(),
                type=DeviceType.LIFX,
                power_state=PowerState.ON if d.get_power() else PowerState.OFF,
                room=room
            )
        )

    if not devices:
        LOGGER.info("No Lifx devices found")

    return results

def _connect(config: DeviceConfig) -> Light:
    light = Light(config.mac, str(config.ip)) 
    return light

def control_lifx_device(config: DeviceConfig, action: PowerAction) -> PowerState:
    device = _connect(config)
    match action:
        case PowerAction.ON:
            device.set_power("on")
            return PowerState.ON
        case PowerAction.OFF:
            device.set_power("off")
            return PowerState.OFF
        case PowerAction.TOGGLE:
            if device.get_power():
                device.set_power("off")
                return PowerState.OFF
            else:
                device.set_power("on")
                return PowerState.ON

def update_lifx_device_name(config: DeviceConfig, new_name: str) -> str:
    device = _connect(config)
    device.set_label(new_name)
    return new_name

def get_lifx_device_power_state(config: DeviceConfig) -> PowerState:
    device = _connect(config)
    return PowerState.ON if device.get_power() else PowerState.OFF
