from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from app.repositories import FavoritesRepository, SearchCacheRepository, UserProfileRepository
from app.schemas import Event, Favorite, UserProfile


class MongoSearchCacheRepository(SearchCacheRepository):
    """Mongo-backed search cache for events."""

    def __init__(self, collection: AsyncIOMotorCollection, ttl_seconds: int) -> None:
        self.collection = collection
        self.ttl_seconds = ttl_seconds

    async def get(self, key: str) -> Optional[List[Event]]:
        doc = await self.collection.find_one({"_id": key})
        if not doc:
            return None
        # Convert stored dicts back to Event models
        return [Event(**item) for item in doc["events"]]

    async def set(self, key: str, events: List[Event]) -> None:
        await self.collection.replace_one(
            {"_id": key},
            {
                "_id": key,
                "events": [event.model_dump() for event in events],
                "created_at": datetime.now(timezone.utc),
            },
            upsert=True,
        )
        await self.collection.create_index("created_at", expireAfterSeconds=self.ttl_seconds)


class MongoUserProfileRepository(UserProfileRepository, FavoritesRepository):
    """Mongo-backed user profiles and favorites."""

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    async def get(self, user_id: str) -> Optional[UserProfile]:
        doc = await self.collection.find_one({"_id": user_id})
        if not doc:
            return None
        return UserProfile(**doc)

    async def upsert(self, profile: UserProfile) -> UserProfile:
        payload = profile.model_dump()
        payload["_id"] = payload.pop("user_id")
        await self.collection.replace_one({"_id": payload["_id"]}, payload, upsert=True)
        return profile

    async def list(self, user_id: str) -> List[Favorite]:
        profile = await self.get(user_id)
        return profile.favorites if profile else []

    async def upsert_favorite(self, user_id: str, favorite: Favorite) -> Favorite:
        profile = await self.get(user_id) or UserProfile(user_id=user_id, email=f"{user_id}@example.com", favorites=[])
        if favorite not in profile.favorites:
            profile.favorites.append(favorite)
        await self.upsert(profile)
        return favorite

    async def delete_favorite(self, user_id: str, favorite: Favorite) -> None:
        profile = await self.get(user_id)
        if not profile:
            return
        profile.favorites = [f for f in profile.favorites if f != favorite]
        await self.upsert(profile)
