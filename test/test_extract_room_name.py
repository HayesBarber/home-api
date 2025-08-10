from app.services.device_service import extract_room_name
from app.config import settings

def test_extract_room_name():
    room, name = extract_room_name("Light --bedroom-- Main")
    assert room == "bedroom"
    assert name == "Main"

    room, name = extract_room_name("--kitchen-- Ceiling")
    assert room == "kitchen"
    assert name == "Ceiling"

    room, name = extract_room_name("Lamp --office--")
    assert room == "office"
    assert name == ""

    room, name = extract_room_name("Desk Lamp")
    assert room == settings.default_room
    assert name == "Desk Lamp"

    room, name = extract_room_name("Light --bedroom")
    assert room == settings.default_room
    assert name == "Light --bedroom"

if __name__ == "__main__":
    test_extract_room_name()
