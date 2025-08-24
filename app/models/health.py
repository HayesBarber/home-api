from enum import Enum
from pydantic import BaseModel

class HealthState(str, Enum):
    HEALTHY = "healthy"
    MODERATE = "moderate"
    UNHEALTHY = "unhealthy"

class HealthResponse(BaseModel):
    state: HealthState

class HealthRequest(BaseModel):
    passcode: str
    port: int
