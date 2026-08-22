"""Tests for the local League Live Client integration."""

import httpx
import pytest

from riftpilot_analytics.clients.live_client import (
    LiveClient,
    LiveClientResponseError,
    LiveClientUnavailableError,
)


def test_get_active_player_returns_validated_data() -> None:
    payload = {
        "currentGold": 1234.0,
        "level": 10,
        "riotId": "Player#BR1",
        "riotIdGameName": "Player",
        "riotIdTagLine": "BR1",
        "championStats": {"attackDamage": 99.0},
    }

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    with LiveClient(transport=httpx.MockTransport(handler)) as client:
        player = client.get_active_player()

    assert player.current_gold == 1234.0
    assert player.level == 10
    assert player.riot_id == "Player#BR1"


def test_get_active_player_maps_connection_failure() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused", request=request)

    with LiveClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(LiveClientUnavailableError):
            client.get_active_player()


def test_get_active_player_rejects_invalid_payload() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"level": 1})

    with LiveClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(LiveClientResponseError):
            client.get_active_player()
