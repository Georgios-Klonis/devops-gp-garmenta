from __future__ import annotations

import logging
from typing import Optional

from fastapi import Depends, Header
from jose import JWTError, jwt

from app.schemas import UserContext
from common.config import get_settings
from common.errors import UnauthorizedError


def get_current_user(authorization: str | None = Header(default=None), settings=Depends(get_settings)) -> UserContext:
    """Validate JWT if configured; fallback to static token for local dev."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise UnauthorizedError("Missing bearer token")

    token = authorization.split(" ", 1)[1]
    if settings.jwt_secret:
        return _decode_jwt(token, settings.jwt_secret, settings.jwt_issuer, settings.jwt_audience)

    if token != settings.auth_demo_token:
        raise UnauthorizedError("Invalid token")

    return UserContext(user_id="demo-user", email="demo@ticketwise.com")


def _decode_jwt(token: str, secret: str, issuer: Optional[str], audience: Optional[str]) -> UserContext:
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            issuer=issuer,
            audience=audience,
        )
    except JWTError as exc:
        logging.getLogger(__name__).warning("JWT validation failed: %s", exc)
        raise UnauthorizedError("Invalid token")

    user_id = payload.get("sub") or payload.get("oid")
    email = payload.get("email")
    if not user_id or not email:
        raise UnauthorizedError("Invalid token payload")

    return UserContext(user_id=str(user_id), email=email)
