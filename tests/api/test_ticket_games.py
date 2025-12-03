from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.main import app  # noqa: E402
from app.dependencies import get_ticket_finder_service  # noqa: E402


class StubTicketFinder:
    def __init__(self, output: str = "stub-output") -> None:
        self.output = output
        self.calls = 0

    def find_tickets(self, **kwargs) -> str:
        self.calls += 1
        return self.output


def test_get_ticket_games_uses_ticket_finder(monkeypatch):
    stub = StubTicketFinder(output='{"ok": true}')
    app.dependency_overrides[get_ticket_finder_service] = lambda: stub
    client = TestClient(app)

    resp = client.post(
        "/v1/getTicketGames",
        json={
            "team_1": "Real Madrid",
            "team_2": "Barcelona",
            "date_from": "2025-01-01",
            "date_to": "2025-02-01",
            "price_from": "50",
            "price_to": "150",
            "preferred_vendors": ["Ticketmaster", "StubHub"],
        },
    )

    assert resp.status_code == 200
    assert resp.json() == {"ok": True}
    assert stub.calls == 1

    app.dependency_overrides.clear()
