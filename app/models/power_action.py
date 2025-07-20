from enum import Enum

class PowerAction(str, Enum):
    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"
