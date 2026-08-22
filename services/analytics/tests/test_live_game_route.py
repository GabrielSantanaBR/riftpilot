"""Tests for the RiftPilot live-game status route."""

from fastapi.testclient import TestClient

from riftpilot_analytics.api.routes import live_game
from riftpilot_analytics.clients.live_client import (
    LiveClientResponseError,
    LiveClientUnavailableError,
)
from riftpilot_analytics.main import app
from riftpilot_analytics.models.active_player import ActivePlayer

client = TestClient(app)


class FakeLiveClient:
    """Controllable Live Client replacement used by route tests."""

    def __init__(self, result: ActivePlayer | Exception) -> None:
        self.result = result

    def __enter__(self) -> "FakeLiveClient":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def get_active_player(self) -> ActivePlayer:
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_live_game_status_active(monkeypatch) -> None:
    player = ActivePlayer.model_validate(
        {
            "currentGold": 900,
            "level": 8,
            "riotId": "Player#BR1",
            "championStats": {},
        }
    )
    monkeypatch.setattr(live_game, "LiveClient", lambda: FakeLiveClient(player))

    response = client.get("/live-game/status")

    assert response.status_code == 200
    assert response.json()["status"] == "active"
    assert response.json()["active_player"]["currentGold"] == 900


def test_live_game_status_inactive(monkeypatch) -> None:
    monkeypatch.setattr(
        live_game,
        "LiveClient",
        lambda: FakeLiveClient(LiveClientUnavailableError()),
    )

    response = client.get("/live-game/status")

    assert response.status_code == 200
    assert response.json()["status"] == "inactive"


def test_live_game_status_error(monkeypatch) -> None:
    monkeypatch.setattr(
        live_game,
        "LiveClient",
        lambda: FakeLiveClient(LiveClientResponseError()),
    )

    response = client.get("/live-game/status")

    assert response.status_code == 200
    assert response.json()["status"] == "error"
