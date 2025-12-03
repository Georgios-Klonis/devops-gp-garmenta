from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_ROOT = PROJECT_ROOT / "src" / "backend" / "services" / "api-service"
if str(SERVICE_ROOT) not in sys.path:
    sys.path.append(str(SERVICE_ROOT))

from app.services import TicketFinderService  # noqa: E402


class FakeResponse:
    def __init__(self, text: str) -> None:
        self.output_text = text


class FakeResponsesClient:
    def __init__(self) -> None:
        self.called_with = None
        self.responses = self

    def create(self, **kwargs):
        self.called_with = kwargs
        return FakeResponse("responses-output")


class FakeChatChoices:
    def __init__(self, content: str) -> None:
        self.message = type("msg", (), {"content": content})


class FakeChatCompletion:
    def __init__(self, content: str) -> None:
        self.choices = [FakeChatChoices(content)]


class FakeChatClient:
    def __init__(self) -> None:
        self.called_with = None
        self.chat = self
        self.completions = self

    def create(self, **kwargs):
        self.called_with = kwargs
        return FakeChatCompletion("chat-output")


def test_ticket_finder_uses_responses_when_available(tmp_path):
    client = FakeResponsesClient()
    service = TicketFinderService(client=client, model="test-model", use_websearch=True)

    out = service.find_tickets(team_1="Team A", team_2="Team B", preferred_vendors=["V1"])

    assert out == "responses-output"
    assert client.called_with is not None
    assert client.called_with["model"] == "test-model"
    assert "Team A" in client.called_with["input"]


def test_ticket_finder_falls_back_to_chat(tmp_path):
    client = FakeChatClient()
    service = TicketFinderService(client=client, model="test-model", use_websearch=False)

    out = service.find_tickets(team_1="Team A")

    assert out == "chat-output"
    assert client.called_with is not None
    assert client.called_with["model"] == "test-model"
    assert "Team A" in client.called_with["messages"][0]["content"]
