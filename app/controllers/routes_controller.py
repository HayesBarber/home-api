from fastapi import APIRouter, Response, status
from app.models.upstream import UpstreamMapping
from app.services import routes_service
from app.models import GetAllRoutesResponse

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.get("", response_model=GetAllRoutesResponse)
async def get_routes():
    return routes_service.get_all_routes()


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def upsert_route(req: UpstreamMapping):
    routes_service.upsert_route(req)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(req: UpstreamMapping):
    routes_service.delete_route(req)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
