from fastapi import APIRouter
from app.services import health_service
from app.models import HealthResponse, HealthRequest

router = APIRouter(prefix="/health", tags=["Health"])

@router.post("", response_model=HealthResponse)
async def get_health(req: HealthRequest):
    return await health_service.get_health_state(req)
