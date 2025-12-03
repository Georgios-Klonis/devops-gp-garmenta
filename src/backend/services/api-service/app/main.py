from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import router
from common.config import get_settings
from common.errors import APIError
from common.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.api_title,
    description="FastAPI gateway for TicketWise search, provider aggregation, and health endpoints.",
    version=settings.api_version,
)

# Configure CORS for early development; narrow before production rollout.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    return {"status": "ok", "service": "api-service", "env": settings.env}


@app.get("/")
async def root():
    return {"message": "TicketWise API Service is running", "version": settings.api_version}


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Return JSON response based on APIError.* sub-classes."""
    logging.getLogger(__name__).warning("APIError raised", exc_info=exc)
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
