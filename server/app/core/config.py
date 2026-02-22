from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Starter"
    DATABASE_URL: str
    DATABASE_TYPE: str = "sqlite"  # sqlite, mysql, postgres (sync/async)

    # Example: postgresql+asyncpg://user:pass@host/db
    # Example: sqlite+aiosqlite:///./test.db
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()