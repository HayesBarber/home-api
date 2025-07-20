from app.models import CreateThemeRequest, DeleteThemeRequest, GetThemesResponse
from app.utils.redis_client import redis_client, Namespace

def save_theme(req: CreateThemeRequest) -> None:
    redis_client.set(Namespace.THEME, req.name, req.colors)

def get_all_themes() -> GetThemesResponse:
    pass

def delete_theme(req: DeleteThemeRequest) -> None:
    pass