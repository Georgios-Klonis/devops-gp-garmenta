from __future__ import annotations

import sys
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.repositories import InMemorySearchCache, ProviderRepository
from app.schemas import Currency, Event, Price, SearchRequest, SeatDetails, TicketListing
from app.services import SearchService
from common.normalization import dedupe_events, sort_events


class CountingProvider(ProviderRepository):
    def __init__(self) -> None:
        self.calls = 0
        self.events: List[Event] = [
            Event(
                event_id="evt-100",
                title="Stub Event",
                league="Test",
                venue="Test Venue",
                start_at=datetime.now(timezone.utc),
                teams=["A", "B"],
                listings=[
                    TicketListing(
                        listing_id="list-1",
                        provider="counting",
                        url="http://example.com/1",
                        price=Price(amount=100, currency=Currency.USD),
                        seat=SeatDetails(),
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            )
        ]

    async def search(self, request: SearchRequest) -> List[Event]:
        self.calls += 1
        return self.events

    async def status(self):
        return []


def test_search_service_caches_results():
    provider = CountingProvider()
    cache = InMemorySearchCache(ttl_seconds=10)
    service = SearchService(provider_repository=provider, cache_repository=cache)

    request = SearchRequest(query="Stub")

    result_first = asyncio.run(service.search(request))
    result_second = asyncio.run(service.search(request))

    assert result_first.total == result_second.total == 1
    assert provider.calls == 1


def test_best_price_marking():
    provider = CountingProvider()
    provider.events[0].listings = [
        TicketListing(
            listing_id="list-1",
            provider="counting",
            url="http://example.com/1",
            price=Price(amount=100, currency=Currency.USD),
            seat=SeatDetails(),
            fetched_at=datetime.now(timezone.utc),
        ),
        TicketListing(
            listing_id="list-2",
            provider="counting",
            url="http://example.com/2",
            price=Price(amount=60, currency=Currency.GBP),  # should win after conversion
            seat=SeatDetails(),
            fetched_at=datetime.now(timezone.utc),
        ),
    ]

    service = SearchService(provider_repository=provider, cache_repository=None)
    result = asyncio.run(service.search(SearchRequest(query="Stub")))

    listings = result.results[0].listings
    best = [l for l in listings if l.is_best_price]
    assert len(best) == 1
    assert best[0].listing_id == "list-2"


class AggregateProvider(ProviderRepository):
    def __init__(self) -> None:
        self.events = [
            Event(
                event_id="dup-1",
                title="B Event",
                league="L1",
                venue="V1",
                start_at=datetime(2024, 5, 1, tzinfo=timezone.utc),
                teams=["X"],
                listings=[
                    TicketListing(
                        listing_id="list-10",
                        provider="p1",
                        url="http://example.com/10",
                        price=Price(amount=50, currency=Currency.USD),
                        seat=SeatDetails(),
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
            Event(
                event_id="dup-1",
                title="B Event",
                league="L1",
                venue="V1",
                start_at=datetime(2024, 5, 1, tzinfo=timezone.utc),
                teams=["X"],
                listings=[
                    TicketListing(
                        listing_id="list-11",
                        provider="p2",
                        url="http://example.com/11",
                        price=Price(amount=45, currency=Currency.USD),
                        seat=SeatDetails(),
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
            Event(
                event_id="unique-2",
                title="A Event",
                league="L1",
                venue="V1",
                start_at=datetime(2024, 4, 1, tzinfo=timezone.utc),
                teams=["X"],
                listings=[
                    TicketListing(
                        listing_id="list-12",
                        provider="p3",
                        url="http://example.com/12",
                        price=Price(amount=30, currency=Currency.USD),
                        seat=SeatDetails(),
                        fetched_at=datetime.now(timezone.utc),
                    )
                ],
            ),
        ]

    async def search(self, request: SearchRequest) -> List[Event]:
        return self.events

    async def status(self):
        return []


def test_normalization_dedupes_and_sorts():
    provider = AggregateProvider()
    service = SearchService(provider_repository=provider, cache_repository=None)

    result = asyncio.run(service.search(SearchRequest(query="anything")))
    events = result.results

    assert len(events) == 2
    assert events[0].event_id == "unique-2"  # earlier start_at sorted first
    assert events[1].event_id == "dup-1"

    # ensure dedup kept only one listing set (first occurrence)
    assert len(events[1].listings) == 1
