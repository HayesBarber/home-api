from app.models import CreateThemeRequest
from app.utils.redis_client import redis_client, Namespace

def save_theme(req: CreateThemeRequest):
    redis_client.set_model(Namespace.THEME, req.name, req)
