"""
Application configuration loaded from environment variables.
Uses pydantic-settings so values are validated at startup.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI API Service"
    environment: str = "development"
    log_level: str = "INFO"

    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Single shared settings instance, imported wherever config is needed
settings = Settings()
