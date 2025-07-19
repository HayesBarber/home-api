import socket
import asyncio

async def discover_esp_devices(passcode: str, port: int):
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', 8000))
    sock.setblocking(False)

    try:
        await loop.sock_sendto(sock, passcode.encode(), ('255.255.255.255', port))
    finally:
        sock.close()
