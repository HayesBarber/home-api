import os

DISCOVERY_INTERVAL_SECONDS = float(os.getenv("DISCOVERY_INTERVAL_SECONDS", "300"))
num_of_lifx_lights_str = os.getenv("NUM_OF_LIFX_LIGHTS")
NUM_OF_LIFX_LIGHTS = int(num_of_lifx_lights_str) if num_of_lifx_lights_str is not None else None
if NUM_OF_LIFX_LIGHTS is not None and NUM_OF_LIFX_LIGHTS < 0:
    raise ValueError("NUM_OF_LIFX_LIGHTS must be a non-negative integer")
