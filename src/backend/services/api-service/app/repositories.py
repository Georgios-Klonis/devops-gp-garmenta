from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Protocol, Sequence

import httpx

from app.schemas import (
    Currency,
    Event,
    Favorite,
    Price,
    ProviderHealth,
    ProviderStatus,
    SearchRequest,
    SeatDetails,
    TicketListing,
    UserProfile,
)


class ProviderRepository(Protocol):
    async def search(self, request: SearchRequest) -> List[Event]:
        """Return normalized events with listings that satisfy the search request."""

    async def status(self) -> List[ProviderStatus]:
        """Return provider health snapshots."""


class SearchCacheRepository(Protocol):
    async def get(self, key: str) -> Optional[List[Event]]:
        """Return cached events for the given key."""

    async def set(self, key: str, events: List[Event]) -> None:
        """Cache a collection of events."""


class UserProfileRepository(Protocol):
    async def get(self, user_id: str) -> Optional[UserProfile]:
        """Return a user profile."""

    async def upsert(self, profile: UserProfile) -> UserProfile:
        """Create or update a profile."""


class FavoritesRepository(Protocol):
    async def list(self, user_id: str) -> List[Favorite]:
        """Return favorites for a user."""

    async def upsert_favorite(self, user_id: str, favorite: Favorite) -> Favorite:
        """Add or update a favorite."""

    async def delete_favorite(self, user_id: str, favorite: Favorite) -> None:
        """Remove a favorite."""


class InMemoryProviderRepository:
    """Simple in-memory provider to unblock early integration work."""

    def __init__(self) -> None:
        self.provider_id = "sample-tickets"
        self._events: List[Event] = [
            Event(
                event_id="evt-001",
                title="Barcelona vs Real Madrid",
                league="La Liga",
                venue="Camp Nou, Barcelona",
                start_at=datetime(2024, 9, 14, 19, 30, tzinfo=timezone.utc),
                teams=["FC Barcelona", "Real Madrid"],
                listings=[
                    TicketListing(
                        listing_id="list-001",
                        provider=self.provider_id,
                        url="https://tickets.example.com/barca-real",
                        price=Price(amount=125.0, currency=Currency.EUR),
                        seat=SeatDetails(section="Lower", row="12", seat="18"),
                        is_best_price=True,
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
            Event(
                event_id="evt-002",
                title="New York Yankees vs Boston Red Sox",
                league="MLB",
                venue="Yankee Stadium, New York",
                start_at=datetime(2024, 7, 2, 18, 10, tzinfo=timezone.utc),
                teams=["New York Yankees", "Boston Red Sox"],
                listings=[
                    TicketListing(
                        listing_id="list-002",
                        provider=self.provider_id,
                        url="https://tickets.example.com/yankees-redsox",
                        price=Price(amount=85.0, currency=Currency.USD),
                        seat=SeatDetails(section="Main", row="7", seat="4"),
                        is_best_price=True,
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
            Event(
                event_id="evt-003",
                title="Los Angeles Lakers vs Golden State Warriors",
                league="NBA",
                venue="Crypto.com Arena, Los Angeles",
                start_at=datetime(2024, 11, 10, 20, 0, tzinfo=timezone.utc),
                teams=["Los Angeles Lakers", "Golden State Warriors"],
                listings=[
                    TicketListing(
                        listing_id="list-003",
                        provider=self.provider_id,
                        url="https://tickets.example.com/lakers-warriors",
                        price=Price(amount=190.0, currency=Currency.USD),
                        seat=SeatDetails(section="200", row="C"),
                        is_best_price=True,
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
        ]

    async def search(self, request: SearchRequest) -> List[Event]:
        query = request.query.lower().strip() if request.query else None
        filters = request.filters

        matched: List[Event] = []
        for event in self._events:
            if query and not self._matches_query(event, query):
                continue
            if filters.team and not any(filters.team.lower() in team.lower() for team in event.teams):
                continue
            if filters.league and (not event.league or filters.league.lower() not in event.league.lower()):
                continue
            if filters.location and (not event.venue or filters.location.lower() not in event.venue.lower()):
                continue
            if filters.date_from and event.start_at < filters.date_from:
                continue
            if filters.date_to and event.start_at > filters.date_to:
                continue

            matched.append(event)
            if len(matched) >= request.limit:
                break

        return matched

    @staticmethod
    def _matches_query(event: Event, query: str) -> bool:
        haystack = [event.title, event.league or "", event.venue or ""] + event.teams
        return any(query in value.lower() for value in haystack)

    async def status(self) -> List[ProviderStatus]:
        now = datetime.now(timezone.utc)
        return [
            ProviderStatus(
                provider_id=self.provider_id,
                status=ProviderHealth.HEALTHY,
                last_success_at=now,
                latency_ms=120,
            )
        ]


class InMemorySearchCache(SearchCacheRepository):
    """In-memory TTL cache for search results."""

    def __init__(self, ttl_seconds: int = 120) -> None:
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[float, List[Event]]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[List[Event]]:
        async with self._lock:
            record = self._cache.get(key)
            if record is None:
                return None

            expires_at, events = record
            if expires_at < time.time():
                self._cache.pop(key, None)
                return None
            return events

    async def set(self, key: str, events: List[Event]) -> None:
        async with self._lock:
            self._cache[key] = (time.time() + self.ttl_seconds, events)


class InMemoryUserProfileRepository(UserProfileRepository, FavoritesRepository):
    """Temporary in-memory store for user profiles and favorites."""

    def __init__(self) -> None:
        self._profiles: Dict[str, UserProfile] = {}

    async def get(self, user_id: str) -> Optional[UserProfile]:
        return self._profiles.get(user_id)

    async def upsert(self, profile: UserProfile) -> UserProfile:
        self._profiles[profile.user_id] = profile
        return profile

    async def list(self, user_id: str) -> List[Favorite]:
        profile = self._profiles.get(user_id)
        return profile.favorites if profile else []

    async def upsert_favorite(self, user_id: str, favorite: Favorite) -> Favorite:
        profile = self._profiles.get(user_id)
        if not profile:
            profile = UserProfile(user_id=user_id, email=f"{user_id}@example.com", favorites=[])
            self._profiles[user_id] = profile
        if favorite not in profile.favorites:
            profile.favorites.append(favorite)
        return favorite

    async def delete_favorite(self, user_id: str, favorite: Favorite) -> None:
        profile = self._profiles.get(user_id)
        if not profile:
            return
        profile.favorites = [f for f in profile.favorites if f != favorite]


@dataclass
class HttpProviderConfig:
    provider_id: str
    base_url: str
    timeout_seconds: float = 5.0


class HttpProviderRepository(ProviderRepository):
    """HTTP-based provider client with basic retry/backoff stub."""

    def __init__(self, config: HttpProviderConfig) -> None:
        self.config = config
        self._last_error: Optional[str] = None
        self._last_success_at: Optional[datetime] = None

    async def search(self, request: SearchRequest) -> List[Event]:
        params = request.model_dump(exclude_none=True)
        try:
            async with httpx.AsyncClient(base_url=self.config.base_url, timeout=self.config.timeout_seconds) as client:
                response = await client.get("/events", params=params)
                response.raise_for_status()
                raw_events = response.json()
                events = [self._to_event(item) for item in raw_events]
                self._last_success_at = datetime.now(timezone.utc)
                return events[: request.limit]
        except Exception as exc:  # pragma: no cover - network failures handled as stub
            self._last_error = str(exc)
            raise

    async def status(self) -> List[ProviderStatus]:
        status = ProviderHealth.HEALTHY if self._last_error is None else ProviderHealth.DEGRADED
        return [
            ProviderStatus(
                provider_id=self.config.provider_id,
                status=status,
                last_success_at=self._last_success_at,
                last_error=self._last_error,
            )
        ]

    def _to_event(self, payload: Dict[str, object]) -> Event:
        # Minimal mapping stub; real implementation will normalize provider-specific fields.
        listings_payload = payload.get("listings", [])
        listings = []
        for item in listings_payload:
            listings.append(
                TicketListing(
                    listing_id=str(item.get("listing_id")),
                    provider=self.config.provider_id,
                    url=str(item.get("url")),
                    price=Price(amount=float(item.get("price", 0)), currency=Currency(item.get("currency", "USD"))),
                    seat=SeatDetails(section=item.get("section"), row=item.get("row"), seat=item.get("seat")),
                    is_best_price=bool(item.get("is_best_price", False)),
                    fetched_at=datetime.now(timezone.utc),
                )
            )

        raw_start = payload.get("start_at") or datetime.now(timezone.utc).isoformat()
        return Event(
            event_id=str(payload.get("event_id")),
            title=str(payload.get("title")),
            league=payload.get("league"),
            venue=payload.get("venue"),
            start_at=datetime.fromisoformat(str(raw_start)),
            teams=list(payload.get("teams", [])),
            listings=listings,
        )


class CompositeProviderRepository(ProviderRepository):
    """Aggregates multiple provider repositories."""

    def __init__(self, providers: Sequence[ProviderRepository]) -> None:
        self.providers = list(providers)

    async def search(self, request: SearchRequest) -> List[Event]:
        results: List[Event] = []
        for provider in self.providers:
            events = await provider.search(request)
            results.extend(events)
            if len(results) >= request.limit:
                break
        return results[: request.limit]

    async def status(self) -> List[ProviderStatus]:
        statuses: List[ProviderStatus] = []
        for provider in self.providers:
            statuses.extend(await provider.status())
        return statuses
