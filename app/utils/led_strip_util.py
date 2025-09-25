from app.models import ControllableDevice, PowerState, PowerAction
from app.utils.esp_util import send_esp_command


async def control_led_strip(
    config: ControllableDevice, action: PowerAction
) -> PowerState:
    payload = {"action": action.value}
    response_text = await send_esp_command(config, payload, action.value)
    return PowerState.ON if response_text == "on" else PowerState.OFF


async def set_led_theme(config: ControllableDevice, colors: str) -> PowerState:
    payload = {"action": "fill", "colors": colors}
    response_text = await send_esp_command(config, payload, "fill")
    return PowerState.ON if response_text == "on" else PowerState.OFF
