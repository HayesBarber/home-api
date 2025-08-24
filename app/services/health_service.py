import asyncio
from app.models import HealthResponse, HealthRequest, HealthState, ControllableDevice, InterfaceDevice
from app.services.discovery_service import (
    discover_lifx,
    discover_kasa,
    discover_esp,
    get_devices_that_checked_in_since_timestamp,
)
from app.utils.redis_client import redis_client, Namespace
from app.utils.logger import LOGGER

async def get_health_state(req: HealthRequest) -> HealthResponse:
    expected_controllables = redis_client.get_all_models(Namespace.CONTROLLABLE_DEVICES, ControllableDevice)
    expected_interfaces = redis_client.get_all_models(Namespace.INTERFACE_DEVICES, InterfaceDevice)
    expected_total = len(expected_controllables) + len(expected_interfaces)

    start_time = LOGGER.get_now()

    try:
        await asyncio.gather(
            discover_lifx(),
            discover_kasa(),
            discover_esp(req.passcode, req.port),
        )

        discovered = get_devices_that_checked_in_since_timestamp(start_time)
        discovered_total = len(discovered.controllable_devices) + len(discovered.interface_devices)

        if discovered_total == 0:
            state = HealthState.UNHEALTHY
        elif discovered_total < expected_total:
            state = HealthState.MODERATE
        else:
            state = HealthState.HEALTHY

        return HealthResponse(state=state)
    except Exception as e:
        LOGGER.error(f"Error in get_health_state: {e}")
        return HealthResponse(state=HealthState.UNHEALTHY)
