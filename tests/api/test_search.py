from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Ensure the service package is importable when running tests from repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_search_returns_results_with_query():
    response = client.post("/v1/search", json={"query": "Barcelona"})
    assert response.status_code == 200

    payload = response.json()
    assert payload["total"] >= 1
    titles = [event["title"] for event in payload["results"]]
    assert any("Barcelona" in title for title in titles)


def test_search_requires_query_or_filters():
    response = client.post("/v1/search", json={"limit": 5})
    assert response.status_code == 422


def test_provider_status_endpoint():
    response = client.get("/v1/providers/status")
    assert response.status_code == 200

    payload = response.json()
    assert payload["providers"]
    assert payload["providers"][0]["provider_id"] == "sample-tickets"


def test_search_filters_by_league():
    response = client.post("/v1/search", json={"filters": {"league": "NBA"}})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["results"][0]["league"] == "NBA"
