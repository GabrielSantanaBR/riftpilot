from riftpilot_analytics.domain.models import SnapshotSource, Team
from riftpilot_analytics.ingestion.live_client import normalize_all_game_data


def test_normalize_live_client_payload() -> None:
    payload = {
        "activePlayer": {"riotId": "Player#BR1", "currentGold": 900, "championStats": {"currentHealth": 800, "maxHealth": 1000, "armor": 50, "magicResist": 40}},
        "allPlayers": [
            {"riotId": "Player#BR1", "championName": "Ahri", "team": "ORDER", "level": 8, "scores": {"kills": 2, "deaths": 1, "assists": 3, "creepScore": 80}, "items": [{"itemID": 1001, "displayName": "Boots", "count": 1, "price": 300}]},
            {"riotId": "Enemy#BR1", "championName": "Annie", "team": "CHAOS", "level": 8, "scores": {}, "items": []},
        ],
        "gameData": {"gameTime": 600, "gameMode": "CLASSIC", "mapName": "Map11"},
        "events": {"Events": [{"EventID": 4, "EventName": "ChampionKill", "EventTime": 590, "KillerName": "Enemy#BR1", "VictimName": "Player#BR1", "Assistants": []}]},
    }
    snapshot = normalize_all_game_data(payload)
    assert snapshot.source == SnapshotSource.LIVE_CLIENT
    assert snapshot.active_player().team == Team.ORDER
    assert snapshot.active_player().stats.health_ratio == 0.8
    assert snapshot.active_player().items[0].name == "Boots"
    assert snapshot.events[0].victim == "Player#BR1"
    assert "Assistants" in snapshot.events[0].payload


def test_normalize_minimal_payload_still_builds_snapshot() -> None:
    snapshot = normalize_all_game_data({"activePlayerName": "Fallback#BR1"})
    assert snapshot.active_player_id == "Fallback#BR1"
    assert len(snapshot.players) == 1
