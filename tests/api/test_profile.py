from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient
from jose import jwt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.main import app  # noqa: E402
from common.config import reset_settings_cache  # noqa: E402

client = TestClient(app)


def test_profile_requires_auth():
    response = client.get("/v1/profile/me")
    assert response.status_code == 401


def test_profile_returns_default_profile_with_valid_token():
    response = client.get("/v1/profile/me", headers={"Authorization": "Bearer demo-token"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["user_id"] == "demo-user"
    assert payload["email"] == "demo@ticketwise.com"


def test_profile_accepts_valid_jwt(monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("TW_JWT_SECRET", secret)
    monkeypatch.setenv("TW_JWT_ISSUER", "test-issuer")
    monkeypatch.setenv("TW_JWT_AUDIENCE", "test-aud")
    reset_settings_cache()

    token = jwt.encode(
        {"sub": "jwt-user", "email": "jwt@example.com", "iss": "test-issuer", "aud": "test-aud"},
        secret,
        algorithm="HS256",
    )

    response = client.get("/v1/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == "jwt-user"
    assert payload["email"] == "jwt@example.com"

    # cleanup
    monkeypatch.delenv("TW_JWT_SECRET", raising=False)
    monkeypatch.delenv("TW_JWT_ISSUER", raising=False)
    monkeypatch.delenv("TW_JWT_AUDIENCE", raising=False)
    reset_settings_cache()
