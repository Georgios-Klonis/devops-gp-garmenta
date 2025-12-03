from __future__ import annotations

import json
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from app.auth import get_current_user
from app.dependencies import get_profile_service, get_search_service, get_ticket_finder_service
from app.schemas import (
    ProviderStatusResponse,
    GetTicketGamesSchema,
    SearchRequest,
    SearchResponse,
    UserContext,
    UserProfile,
)
from app.services import ProfileService, TicketFinderService, SearchService

router = APIRouter(prefix="/v1", tags=["Api"])


@router.post(
    "/getTicketGames",
    response_model=None,
    status_code=status.HTTP_200_OK,
    summary="Get ticket games via LLM-backed search",
)
async def get_ticket_games(
    request: GetTicketGamesSchema,
    ticket_finder_service: TicketFinderService = Depends(get_ticket_finder_service),
) -> str:
    """Proxy request params into the LLM-backed ticket finder."""
    raw = ticket_finder_service.find_tickets(
        team_1=request.team_1,
        team_2=request.team_2 or "",
        date_from=request.date_from,
        date_to=request.date_to,
        price_from=request.price_from or "",
        price_to=request.price_to or "",
        preferred_vendors=request.preferred_vendors,
    )
    try:
        parsed = json.loads(raw)
        return JSONResponse(content=parsed)
    except Exception:
        return Response(content=raw, media_type="text/plain")


@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search for events and ticket listings",
)
async def search_events(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    """Entry point for event search; backed by provider repository + cache."""
    return await search_service.search(request)


@router.get(
    "/providers/status",
    response_model=ProviderStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get provider connector health status",
)
async def provider_status(
    search_service = Depends(get_search_service),
) -> ProviderStatusResponse:
    statuses = await search_service.providers_status()
    return ProviderStatusResponse(providers=statuses)


@router.get(
    "/profile/me",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK,
    summary="Get current user's profile (auth stub)",
)
async def get_profile(
    user: UserContext = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
) -> UserProfile:
    return await profile_service.get_or_create_profile(user)
