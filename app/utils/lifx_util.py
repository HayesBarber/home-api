from lifxlan import LifxLAN
from app import config
from app.models.device import DeviceConfig, DeviceType, PowerState, PowerAction
from typing import List

_lifx = LifxLAN(config.NUM_OF_LIFX_LIGHTS)

def discover_lifx_devices() -> List[DeviceConfig]:
    print("Discovering Lifx devices...")
    devices = _lifx.get_lights()
    results = []

    for d in devices:
        print(f"Found {d.get_label()} at {d.get_ip_addr()}")
        results.append(
            DeviceConfig(
                name=d.get_label(),
                ip=d.get_ip_addr(),
                type=DeviceType.LIFX,
                power_state=PowerState.ON if d.get_power() else PowerState.OFF,
            )
        )

    if not devices:
        print("No Lifx devices found")

    return results

def control_lifx_device(config: DeviceConfig, action: PowerAction) -> PowerState:
    pass
