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