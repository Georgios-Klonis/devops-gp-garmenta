from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.dependencies import (  # noqa: E402
    get_app_settings,
    get_cache_repository,
    get_user_profile_repository,
)
from app.repositories_mongo import MongoSearchCacheRepository, MongoUserProfileRepository  # noqa: E402


class FakeCollection:
    pass


class FakeDatabase(dict):
    def __getitem__(self, item):
        if item not in self:
            self[item] = FakeCollection()
        return dict.__getitem__(self, item)


@pytest.fixture(autouse=True)
def reset_caches():
    get_app_settings.cache_clear()
    get_cache_repository.cache_clear()
    get_user_profile_repository.cache_clear()
    yield
    get_app_settings.cache_clear()
    get_cache_repository.cache_clear()
    get_user_profile_repository.cache_clear()


def test_cache_repository_uses_mongo_when_enabled(monkeypatch):
    fake_db = FakeDatabase()

    monkeypatch.setenv("TW_MONGODB_URI", "mongodb://fake-uri")
    monkeypatch.setenv("TW_USE_MONGO_CACHE", "true")
    monkeypatch.setenv("TW_SEARCH_CACHE_TTL_SECONDS", "60")

    import app.dependencies as deps  # noqa: E402
    monkeypatch.setattr(deps, "get_database", lambda settings: fake_db)

    repo = get_cache_repository()
    assert isinstance(repo, MongoSearchCacheRepository)


def test_profile_repository_uses_mongo_when_enabled(monkeypatch):
    class DummySettings:
        use_mongo_profiles = True
        mongodb_uri = "mongodb://fake-uri"
        mongodb_db_name = "ticketwise"

    fake_db = FakeDatabase()

    import app.dependencies as deps  # noqa: E402
    monkeypatch.setattr(deps, "get_database", lambda settings: fake_db)
    monkeypatch.setattr(deps, "get_app_settings", lambda: DummySettings())

    get_user_profile_repository.cache_clear()

    repo = get_user_profile_repository()
    assert isinstance(repo, MongoUserProfileRepository)
