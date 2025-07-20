from app.models import CreateThemeRequest, DeleteThemeRequest, GetThemesResponse
from app.utils.redis_client import redis_client, Namespace

def save_theme(req: CreateThemeRequest) -> None:
    redis_client.set(Namespace.THEME, req.name, req.colors)

def get_all_themes() -> GetThemesResponse:
    themes = redis_client.get_all(Namespace.THEME)
    return GetThemesResponse(themes=themes)

def delete_theme(req: DeleteThemeRequest) -> None:
    redis_client.delete(Namespace.THEME, req.name)
