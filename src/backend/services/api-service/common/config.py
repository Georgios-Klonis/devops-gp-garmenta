from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    env: str = Field(default="local", description="Deployment environment name")
    api_title: str = Field(default="TicketWise API Service")
    api_version: str = Field(default="0.1.0")
    cors_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )
    search_cache_ttl_seconds: int = Field(default=120, ge=0)
    enable_stub_data: bool = Field(default=True, description="Enable in-memory provider stub data")
    enable_stub_http_provider: bool = Field(default=False, description="Enable HTTP-based provider stub")
    stub_provider_base_url: Optional[HttpUrl] = Field(
        default=None, description="Base URL for HTTP provider stub (if enabled)"
    )
    auth_demo_token: str = Field(default="demo-token", description="Temporary token for stub auth")
    jwt_secret: Optional[str] = Field(default=None, description="HS256 secret for JWT validation")
    jwt_issuer: Optional[str] = Field(default=None, description="Expected JWT issuer")
    jwt_audience: Optional[str] = Field(default=None, description="Expected JWT audience")
    log_level: str = Field(default="INFO")
    mongodb_uri: Optional[str] = Field(default=None, description="MongoDB connection string")
    mongodb_db_name: str = Field(default="ticketwise", description="MongoDB database name")
    use_mongo_cache: bool = Field(default=False, description="Use MongoDB-backed search cache")
    use_mongo_profiles: bool = Field(default=False, description="Use MongoDB-backed profiles/favorites store")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key for ticket finder")
    openai_model: str = Field(default="gpt-4.1", description="OpenAI model for ticket finder")
    openai_use_websearch: bool = Field(default=True, description="Enable web search tool for ticket finder")

    model_config = SettingsConfigDict(env_prefix="TW_", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


def reset_settings_cache() -> None:
    """Clear cached settings (useful for tests)."""
    get_settings.cache_clear()
