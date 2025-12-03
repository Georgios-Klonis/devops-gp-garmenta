from __future__ import annotations

import hashlib
import json
from typing import List, Optional

from app.repositories import ProviderRepository, SearchCacheRepository, UserProfileRepository
from app.schemas import ProviderStatus, SearchRequest, SearchResponse, UserContext, UserProfile
from common.errors import BadRequestError, NotFoundError
from common.pricing import mark_best_prices
from common.normalization import normalize_events


class SearchService:
    """Coordinates search queries across providers and cache."""

    def __init__(
        self,
        provider_repository: ProviderRepository,
        cache_repository: Optional[SearchCacheRepository] = None,
    ) -> None:
        self.provider_repository = provider_repository
        self.cache_repository = cache_repository

    async def search(self, request: SearchRequest) -> SearchResponse:
        if request.limit <= 0:
            raise BadRequestError("Limit must be a positive integer")

        cache_key = self._cache_key(request) if self.cache_repository else None
        if cache_key and self.cache_repository:
            cached = await self.cache_repository.get(cache_key)
            if cached is not None:
                return SearchResponse.from_events(cached)

        events = await self.provider_repository.search(request)
        mark_best_prices(events)
        events = normalize_events(events)

        if cache_key and self.cache_repository:
            await self.cache_repository.set(cache_key, events)

        return SearchResponse.from_events(events)

    async def providers_status(self) -> List[ProviderStatus]:
        return await self.provider_repository.status()

    @staticmethod
    def _cache_key(request: SearchRequest) -> str:
        serialized = json.dumps(
            request.model_dump(mode="json"),
            sort_keys=True,
            default=str,
        )
        return f"search:{hashlib.sha1(serialized.encode('utf-8')).hexdigest()}"


class ProfileService:
    """User profile and favorites management stub."""

    def __init__(self, user_repository: UserProfileRepository) -> None:
        self.user_repository = user_repository

    async def get_or_create_profile(self, user: UserContext) -> UserProfile:
        profile = await self.user_repository.get(user.user_id)
        if profile:
            return profile

        profile = UserProfile(user_id=user.user_id, email=user.email, favorites=[])
        return await self.user_repository.upsert(profile)

    async def update_profile(self, profile: UserProfile) -> UserProfile:
        return await self.user_repository.upsert(profile)

    async def get_profile(self, user_id: str) -> UserProfile:
        profile = await self.user_repository.get(user_id)
        if not profile:
            raise NotFoundError("Profile not found")
        return profile
