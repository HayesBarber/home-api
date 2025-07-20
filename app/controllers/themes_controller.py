from fastapi import APIRouter
from app.models import ApplyThemeRequest
from app.services import themes_service

router = APIRouter(prefix="/theme", tags=["Themes"])

@router.post("/apply")
async def apply_theme(req: ApplyThemeRequest):
    return await themes_service.set_theme(req)
