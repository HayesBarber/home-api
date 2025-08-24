from fastapi import APIRouter
from app.services import health_service
from app.models import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
def get_health():
    return health_service.get_health_state()
