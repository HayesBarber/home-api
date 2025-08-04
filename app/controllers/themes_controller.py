from fastapi import APIRouter
from app.models import ApplyThemeRequest, CreateThemeRequest, DeleteThemeRequest, GetThemesResponse, DeviceConfig, EffectedDevicesResponse
from app.services import themes_service
from typing import List

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("/apply", response_model=EffectedDevicesResponse)
async def apply_theme(req: ApplyThemeRequest) -> List[DeviceConfig]:
    return await themes_service.set_theme(req)

@router.post("/", response_model=GetThemesResponse)
def create_theme(req: CreateThemeRequest) -> GetThemesResponse:
    return themes_service.save_theme(req)

@router.get("/", response_model=GetThemesResponse)
def get_themes() -> GetThemesResponse:
    return themes_service.get_all_themes()

@router.delete("/", response_model=GetThemesResponse)
def delete_theme(req: DeleteThemeRequest) -> GetThemesResponse:
    return themes_service.delete_theme(req)
