from enum import Enum

class DeviceType(str, Enum):
    KASA = "kasa"
    LIFX = "lifx"
    LED_STRIP = "led_strip"
    INTERFACE = "interface"
