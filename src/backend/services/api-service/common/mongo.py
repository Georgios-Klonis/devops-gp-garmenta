from __future__ import annotations

from functools import lru_cache
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from common.config import AppSettings, get_settings


@lru_cache
def get_client(settings: Optional[AppSettings] = None) -> AsyncIOMotorClient:
    cfg = settings or get_settings()
    if not cfg.mongodb_uri:
        raise ValueError("MongoDB URI is not configured")
    return AsyncIOMotorClient(cfg.mongodb_uri)


def get_database(settings: Optional[AppSettings] = None) -> AsyncIOMotorDatabase:
    cfg = settings or get_settings()
    return get_client(cfg)[cfg.mongodb_db_name]
