from enum import Enum

class HealthState(str, Enum):
    HEALTHY = "healthy"
    MODERATE = "moderate"
    UNHEALTHY = "unhealthy"
