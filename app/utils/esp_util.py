import socket
import asyncio
import httpx
from app.models import ControllableDevice, InterfaceDevice
from app.utils.logger import LOGGER


async def discover_esp_devices(passcode: str, port: int):
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", 8000))
    sock.setblocking(False)

    try:
        await loop.sock_sendto(sock, passcode.encode(), ("255.255.255.255", port))
    finally:
        sock.close()


async def send_esp_command(
    config: ControllableDevice | InterfaceDevice, payload: dict, log_action: str
) -> str | None:
    url = f"http://{config.ip}/message"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=5)
            response.raise_for_status()
            LOGGER.info(
                f"Successfully sent {log_action} to {config.name} at {config.ip}"
            )

            response_text = response.text.strip().lower()
            if not response_text:
                return None

            return response_text
    except httpx.RequestError as exc:
        LOGGER.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return None
    except httpx.HTTPStatusError as exc:
        LOGGER.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc}"
        )
        return None
