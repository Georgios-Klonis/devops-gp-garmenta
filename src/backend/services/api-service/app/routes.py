from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.auth import get_current_user
from app.dependencies import get_profile_service, get_search_service
from app.schemas import ProviderStatusResponse, SearchRequest, SearchResponse, UserContext, UserProfile
from app.services import ProfileService, SearchService

router = APIRouter(prefix="/v1", tags=["Api"])


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
    """Entry point for event search; currently backed by an in-memory provider stub."""
    return await search_service.search(request)


@router.get(
    "/providers/status",
    response_model=ProviderStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get provider connector health status",
)
async def provider_status(
    search_service: SearchService = Depends(get_search_service),
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
