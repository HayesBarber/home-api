import httpx
from app.models.device import DeviceConfig, PowerState, PowerAction
from app.utils.logger import LOGGER

async def _send_led_command(config: DeviceConfig, payload: dict, log_action: str) -> PowerState:
    url = f"http://{config.ip}/message"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=5)
            response.raise_for_status()
            LOGGER.info(f"Successfully sent {log_action} to LED strip at {config.ip}")
            
            response_text = response.text.strip().lower()
            return PowerState.ON if response_text == "on" else PowerState.OFF
    except httpx.RequestError as exc:
        LOGGER.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return config.power_state
    except httpx.HTTPStatusError as exc:
        LOGGER.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}")
        return config.power_state

async def control_led_strip(config: DeviceConfig, action: PowerAction) -> PowerState:
    payload = {"action": action.value}
    return await _send_led_command(config, payload, action.value)

async def set_led_theme(config: DeviceConfig) -> PowerState:
    payload = {"action": "fill", "colors": "todo"}
    return await _send_led_command(config, payload, "fill")
