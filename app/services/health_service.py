import asyncio
from app.models import (
    HealthResponse,
    HealthRequest,
    HealthState,
    ControllableDevice,
    InterfaceDevice,
)
from app.services.discovery_service import (
    discover_lifx,
    discover_kasa,
    discover_esp,
    get_devices_that_checked_in_since_timestamp,
)
from app.utils.redis_client import redis_client, Namespace
from app.utils.logger import LOGGER


async def get_health_state(req: HealthRequest) -> HealthResponse:
    try:
        expected_controllables = redis_client.get_all_models(
            Namespace.CONTROLLABLE_DEVICES, ControllableDevice
        )
        expected_interfaces = redis_client.get_all_models(
            Namespace.INTERFACE_DEVICES, InterfaceDevice
        )
        expected_total = len(expected_controllables) + len(expected_interfaces)

        if expected_total <= 0:
            return HealthResponse(state=HealthState.HEALTHY)

        start_time = LOGGER.get_now()

        await asyncio.gather(
            discover_lifx(),
            discover_kasa(),
            discover_esp(req.passcode, req.port),
        )

        discovered = get_devices_that_checked_in_since_timestamp(start_time)
        discovered_controllables = discovered.controllable_devices
        discovered_interfaces = discovered.interface_devices
        discovered_total = len(discovered_controllables) + len(discovered_interfaces)

        if discovered_total == 0:
            return HealthResponse(
                state=HealthState.UNHEALTHY,
                reason="no_devices_found",
            )

        if discovered_total < expected_total:
            expected_names = {
                name
                for name in expected_controllables.keys() + expected_interfaces.keys()
            }
            discovered_names = {
                d.name for d in discovered_controllables + discovered_interfaces
            }

            missing_names = expected_names - discovered_names

            return HealthResponse(
                state=HealthState.MODERATE,
                reason="some_devices_not_found",
                missing_devices=missing_names,
            )

        return HealthResponse(state=HealthState.HEALTHY)
    except Exception as e:
        LOGGER.error(f"Error in get_health_state: {e}")
        return HealthResponse(state=HealthState.UNHEALTHY, reason="exception")
