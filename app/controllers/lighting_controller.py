from fastapi import APIRouter
from app.services import lighting_service
from app.models import PowerAction, Theme

router = APIRouter(prefix="/lighting", tags=["Lighting"])

@router.get("/{name}/{action}")
async def set_state(name: str, action: PowerAction):
    return await lighting_service.set_state(name, action)

@router.post("/theme")
async def apply_theme(req: Theme):
    return await lighting_service.set_theme(req)
