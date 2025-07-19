import httpx
from app.models.device import DeviceConfig, PowerState, PowerAction
from app.utils.logger import LOGGER

async def control_led_strip(config: DeviceConfig, action: PowerAction) -> PowerState:
    url = f"http://{config.ip}/"
    json_payload = {"action": action.value}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=json_payload, timeout=5)
            response.raise_for_status()
            LOGGER.info(f"Successfully sent {action.value} to LED strip at {config.ip}")
            
            response_text = response.text.strip().lower()
            if response_text == "on":
                return PowerState.ON
            else:
                return PowerState.OFF
    except httpx.RequestError as exc:
        LOGGER.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return config.power_state
    except httpx.HTTPStatusError as exc:
        LOGGER.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}")
        return config.power_state