from fastapi import APIRouter
from app.services import routes_service
from app.models import GetAllRoutesResponse

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.get("", response_model=GetAllRoutesResponse)
async def get_routes():
    return routes_service.get_all_routes()
