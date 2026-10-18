"""
==================================================
CommuteShare Configuration

Backend Internship Project
Bermer Software Private Limited

Centralized application configuration using
Pydantic Settings.

All application settings are loaded from
environment variables or a .env file.
==================================================
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Loaded automatically from:
    - Environment Variables
    - .env file
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "CommuteShare"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    ENVIRONMENT: str = "development"

    # ==========================================================
    # Server
    # ==========================================================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_URL: str

    # ==========================================================
    # JWT Authentication
    # ==========================================================

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Optional OAuth login configuration. Provider logins remain hidden
    # until each provider has both credentials configured.
    GOOGLE_OAUTH_CLIENT_ID: str | None = None
    GOOGLE_OAUTH_CLIENT_SECRET: str | None = None
    GITHUB_OAUTH_CLIENT_ID: str | None = None
    GITHUB_OAUTH_CLIENT_SECRET: str | None = None
    BACKEND_PUBLIC_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://localhost:5173"

    # Optional SMTP configuration used only for password reset emails.
    SMTP_HOST: str | None = None
    SMTP_PORT: int = Field(default=587, ge=1, le=65535)
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str | None = None
    SMTP_USE_SSL: bool = False
    SMTP_STARTTLS: bool = True
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0, le=1440)

    # ==========================================================
    # Password Hashing
    # ==========================================================

    BCRYPT_ROUNDS: int = 12

    # ==========================================================
    # CORS
    # ==========================================================

    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
        ]
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, value):
        """
        Allows CORS origins to be provided either as:

        http://localhost:5173,http://127.0.0.1:5173

        OR

        ["http://localhost:5173"]
        """

        if isinstance(value, str):

            return [origin.strip() for origin in value.split(",")]

        return value

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        """Accept environment names as a safe shorthand for debug mode."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "production", "prod"}:
                return False
            if normalized in {"development", "dev", "debug"}:
                return True
        return value

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_LEVEL: str = "INFO"

    # ==========================================================
    # Ride Matching
    # ==========================================================

    DEFAULT_SEARCH_RADIUS_KM: int = 5

    MAX_ACTIVE_RIDES_PER_DRIVER: int = 3

    # ==========================================================
    # File Upload
    # ==========================================================

    MAX_PROFILE_IMAGE_SIZE_MB: int = 5

    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default_factory=lambda: [
            "jpg",
            "jpeg",
            "png",
            "webp",
        ]
    )

    # ==========================================================
    # Admin
    # ==========================================================

    DEFAULT_ADMIN_EMAIL: str = "admin@commuteshare.com"

    # ==========================================================
    # Pydantic Settings Configuration
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    
@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings object.

    Using lru_cache ensures the .env file
    is loaded only once during application startup.
    """

    return Settings()


settings = get_settings()
