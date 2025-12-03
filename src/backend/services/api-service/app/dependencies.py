from __future__ import annotations

from functools import lru_cache
import os

from common.config import AppSettings, get_settings
from common.mongo import get_database
from app.repositories import (
    CompositeProviderRepository,
    HttpProviderConfig,
    HttpProviderRepository,
    InMemoryProviderRepository,
    InMemorySearchCache,
    InMemoryUserProfileRepository,
    ProviderRepository,
    SearchCacheRepository,
    UserProfileRepository,
)
from app.repositories_mongo import MongoSearchCacheRepository, MongoUserProfileRepository
from app.services import ProfileService, SearchService, TicketFinderService
from openai import OpenAI


@lru_cache
def get_app_settings() -> AppSettings:
    return get_settings()


@lru_cache
def get_provider_repository() -> ProviderRepository:
    settings = get_app_settings()
    providers = []

    if settings.enable_stub_data:
        providers.append(InMemoryProviderRepository())

    if settings.enable_stub_http_provider and settings.stub_provider_base_url:
        providers.append(
            HttpProviderRepository(
                config=HttpProviderConfig(
                    provider_id="stub-http",
                    base_url=str(settings.stub_provider_base_url),
                )
            )
        )

    return CompositeProviderRepository(providers=providers)


@lru_cache
def get_cache_repository() -> SearchCacheRepository:
    settings = get_app_settings()
    if settings.use_mongo_cache and settings.mongodb_uri:
        collection = get_database(settings)["search_cache"]
        return MongoSearchCacheRepository(collection=collection, ttl_seconds=settings.search_cache_ttl_seconds)
    return InMemorySearchCache(ttl_seconds=settings.search_cache_ttl_seconds)


@lru_cache
def get_search_service() -> SearchService:
    return SearchService(
        provider_repository=get_provider_repository(),
        cache_repository=get_cache_repository(),
    )


@lru_cache
def get_user_profile_repository() -> UserProfileRepository:
    settings = get_app_settings()
    if settings.use_mongo_profiles and settings.mongodb_uri:
        collection = get_database(settings)["profiles"]
        return MongoUserProfileRepository(collection=collection)
    return InMemoryUserProfileRepository()


@lru_cache
def get_profile_service() -> ProfileService:
    return ProfileService(user_repository=get_user_profile_repository())


@lru_cache
def get_ticket_finder_service() -> TicketFinderService:
    settings = get_app_settings()
    api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("TW_OPENAI_API_KEY or OPENAI_API_KEY is required for ticket finder.")
    client = OpenAI(api_key=api_key)
    return TicketFinderService(
        client=client,
        model=settings.openai_model,
        use_websearch=settings.openai_use_websearch,
    )
