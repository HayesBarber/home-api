from pydantic_settings import BaseSettings, SettingsConfigDict
from app.utils.logger import LOGGER

class Settings(BaseSettings):
    default_room: str = "Living Room"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

LOGGER.info(f"Loaded settings: {settings.model_dump_json()}")
