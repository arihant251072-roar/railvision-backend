from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://railvision:railvision@localhost:5432/railvision"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # OR-Tools settings
    OR_TOOLS_TIME_LIMIT: int = 30  # seconds

    # Emergency response settings
    EMERGENCY_RADIUS_KM: float = 50.0
    KAVACH_HALT_RADIUS_KM: float = 50.0

    # Health score thresholds
    HEALTH_GREEN_THRESHOLD: float = 0.8
    HEALTH_ORANGE_THRESHOLD: float = 0.6
    HEALTH_RED_THRESHOLD: float = 0.4
    HEALTH_DARK_RED_THRESHOLD: float = 0.2

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()