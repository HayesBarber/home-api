import socket

def discover_esp_devices(passcode: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', 8000))
        sock.sendto(passcode.encode(), ('255.255.255.255', port))
