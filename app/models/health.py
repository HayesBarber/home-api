from enum import Enum
from pydantic import BaseModel


class HealthState(str, Enum):
    HEALTHY = "healthy"
    MODERATE = "moderate"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseModel):
    state: HealthState
    missing_devices: set[str] | None = None
    reason: str | None = None


class HealthRequest(BaseModel):
    passcode: str
    port: int
