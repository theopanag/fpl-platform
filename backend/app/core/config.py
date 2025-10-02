"""
Application configuration settings.

Uses Pydantic settings for environment variable management and validation.
"""

from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    # Environment Detection
    NODE_ENV: str = "development"

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FPL Analytics"

    # Debug and Logging (computed based on NODE_ENV)
    DEBUG: bool | None = None
    LOG_LEVEL: str | None = None

    def __init__(self, **kwargs):
        """Initialize settings with computed DEBUG and LOG_LEVEL based on NODE_ENV."""
        super().__init__(**kwargs)

        # Set DEBUG based on NODE_ENV if not explicitly provided
        if self.DEBUG is None:
            self.DEBUG = self.NODE_ENV.lower() != "production"

        # Set LOG_LEVEL based on NODE_ENV if not explicitly provided
        if self.LOG_LEVEL is None:
            self.LOG_LEVEL = "INFO" if self.NODE_ENV.lower() == "production" else "DEBUG"

    # CORS
    ALLOWED_HOSTS: list[str] = ["http://localhost:8080", "http://localhost:8050"]

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "fpl_analytics"

    @field_validator("POSTGRES_SERVER", mode="before")
    @classmethod
    def get_postgres_server(cls, v: str | None) -> str:
        """Get PostgreSQL server."""
        if v is None:
            return "localhost"
        return v

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """Build database URI."""
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    @property
    def REDIS_URL(self) -> str:
        """Build Redis URL."""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # FPL API
    FPL_API_BASE_URL: str = "https://fantasy.premierleague.com/api"
    FPL_CACHE_DURATION: int = 300  # 5 minutes

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60


settings = Settings()