from fastapi import APIRouter
from app.services import health_service
from app.models import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def get_health():
    return await health_service.get_health_state()
