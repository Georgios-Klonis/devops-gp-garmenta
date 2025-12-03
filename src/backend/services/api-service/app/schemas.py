from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator, model_validator


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class Price(BaseModel):
    amount: float = Field(..., gt=0, description="Numeric value of the ticket price")
    currency: Currency = Field(default=Currency.USD, description="ISO currency for the price")


class SeatDetails(BaseModel):
    section: Optional[str] = Field(default=None, max_length=64)
    row: Optional[str] = Field(default=None, max_length=32)
    seat: Optional[str] = Field(default=None, max_length=32)
    notes: Optional[str] = Field(default=None, max_length=256)


class TicketListing(BaseModel):
    listing_id: str = Field(..., min_length=3, max_length=128)
    provider: str = Field(..., min_length=2, max_length=64)
    url: HttpUrl
    price: Price
    seat: SeatDetails = Field(default_factory=SeatDetails)
    is_best_price: bool = False
    fetched_at: datetime


class Event(BaseModel):
    event_id: str = Field(..., min_length=3, max_length=128)
    title: str = Field(..., min_length=3, max_length=256)
    league: Optional[str] = Field(default=None, max_length=128)
    venue: Optional[str] = Field(default=None, max_length=256)
    start_at: datetime
    teams: List[str] = Field(default_factory=list)
    listings: List[TicketListing] = Field(default_factory=list)


class SearchFilters(BaseModel):
    team: Optional[str] = Field(default=None, max_length=128)
    league: Optional[str] = Field(default=None, max_length=128)
    location: Optional[str] = Field(default=None, max_length=128)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "SearchFilters":
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise ValueError("date_from must be earlier than date_to")
        return self

    def is_empty(self) -> bool:
        return not any(
            [
                self.team,
                self.league,
                self.location,
                self.date_from,
                self.date_to,
            ]
        )


class SearchRequest(BaseModel):
    query: Optional[str] = Field(default=None, min_length=2, max_length=256)
    filters: SearchFilters = Field(default_factory=SearchFilters)
    limit: int = Field(default=25, ge=1, le=100)

    @field_validator("query")
    @classmethod
    def normalize_query(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = value.strip()
        return normalized or None

    @model_validator(mode="after")
    def ensure_search_params(self) -> "SearchRequest":
        if not self.query and self.filters.is_empty():
            raise ValueError("Provide either a search query or at least one filter")
        return self


class SearchResponse(BaseModel):
    results: List[Event]
    total: int

    @classmethod
    def from_events(cls, events: List[Event]) -> "SearchResponse":
        return cls(results=events, total=len(events))


class ProviderHealth(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"


class ProviderStatus(BaseModel):
    provider_id: str = Field(..., min_length=2, max_length=64)
    status: ProviderHealth = ProviderHealth.HEALTHY
    last_success_at: Optional[datetime] = None
    last_error: Optional[str] = Field(default=None, max_length=256)
    latency_ms: Optional[int] = Field(default=None, ge=0)


class ProviderStatusResponse(BaseModel):
    providers: List[ProviderStatus] = Field(default_factory=list)


class FavoriteType(str, Enum):
    TEAM = "team"
    LEAGUE = "league"


class Favorite(BaseModel):
    type: FavoriteType
    name: str = Field(..., min_length=2, max_length=128)
    metadata: Optional[str] = Field(default=None, max_length=256)


class UserProfile(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    favorites: List[Favorite] = Field(default_factory=list)


class UserContext(BaseModel):
    user_id: str
    email: EmailStr
