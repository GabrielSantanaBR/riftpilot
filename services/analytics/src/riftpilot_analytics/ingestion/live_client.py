"""Riot Live Client Data API adapter and normalization."""

from __future__ import annotations

from typing import Any

import httpx

from riftpilot_analytics.domain.models import ChampionStats, GameEvent, GameSnapshot, ItemState, PlayerState, Score, SnapshotSource, Team


class LiveClientUnavailable(RuntimeError):
    """Raised when the local League game client endpoint cannot be reached."""


class LiveClientClient:
    """Small adapter around the local, read-only Live Client Data API."""

    def __init__(self, base_url: str = "https://127.0.0.1:2999/liveclientdata", timeout: float = 1.5) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_all_game_data(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(verify=False, timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/allgamedata")
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LiveClientUnavailable("League live client is not available") from exc

    async def get_snapshot(self) -> GameSnapshot:
        return normalize_all_game_data(await self.get_all_game_data())


def _riot_id(raw: dict[str, Any]) -> str:
    return str(raw.get("riotId") or raw.get("summonerName") or raw.get("riotIdGameName") or "Unknown player")


def _normalize_score(raw: dict[str, Any] | None) -> Score:
    raw = raw or {}
    return Score(kills=int(raw.get("kills", 0)), deaths=int(raw.get("deaths", 0)), assists=int(raw.get("assists", 0)), creep_score=int(raw.get("creepScore", 0)), ward_score=float(raw.get("wardScore", 0.0)))


def _normalize_items(raw_items: list[dict[str, Any]] | None) -> list[ItemState]:
    return [ItemState(item_id=int(item.get("itemID", 0)), name=str(item.get("displayName") or item.get("rawDisplayName") or "Unknown item"), count=int(item.get("count", 1)), price=int(item.get("price", 0))) for item in (raw_items or [])]


def _normalize_stats(raw: dict[str, Any] | None) -> ChampionStats | None:
    if not raw:
        return None
    return ChampionStats(current_health=float(raw.get("currentHealth", 0.0)), max_health=float(raw.get("maxHealth", 0.0)), armor=float(raw.get("armor", 0.0)), magic_resist=float(raw.get("magicResist", 0.0)), attack_damage=float(raw.get("attackDamage", 0.0)), ability_power=float(raw.get("abilityPower", 0.0)), move_speed=float(raw.get("moveSpeed", 0.0)), ability_haste=float(raw.get("abilityHaste", 0.0)))


def _normalize_event(raw: dict[str, Any]) -> GameEvent:
    reserved = {"EventID", "EventName", "EventTime", "KillerName", "VictimName"}
    return GameEvent(event_id=raw.get("EventID"), event_name=str(raw.get("EventName", "UnknownEvent")), event_time=float(raw.get("EventTime", 0.0)), actor=raw.get("KillerName"), victim=raw.get("VictimName"), payload={key: value for key, value in raw.items() if key not in reserved})


def normalize_all_game_data(payload: dict[str, Any]) -> GameSnapshot:
    """Normalize Riot's API-shaped payload into a stable domain snapshot."""
    active_raw = payload.get("activePlayer") or {}
    active_id = str(active_raw.get("riotId") or active_raw.get("summonerName") or payload.get("activePlayerName") or "Unknown player")
    active_stats = _normalize_stats(active_raw.get("championStats"))
    active_gold = active_raw.get("currentGold")

    players: list[PlayerState] = []
    for raw in payload.get("allPlayers") or []:
        riot_id = _riot_id(raw)
        team_raw = str(raw.get("team", "UNKNOWN")).upper()
        team = Team(team_raw) if team_raw in Team._value2member_map_ else Team.UNKNOWN
        players.append(PlayerState(riot_id=riot_id, champion_name=str(raw.get("championName", "Unknown")), team=team, level=int(raw.get("level", 1)), is_active=riot_id == active_id, score=_normalize_score(raw.get("scores")), items=_normalize_items(raw.get("items")), stats=active_stats if riot_id == active_id else None, current_gold=float(active_gold) if riot_id == active_id and active_gold is not None else None))

    if not players:
        players = [PlayerState(riot_id=active_id, champion_name=str(active_raw.get("championName", "Unknown")), is_active=True, stats=active_stats, current_gold=float(active_gold) if active_gold is not None else None)]

    game_data = payload.get("gameData") or {}
    events_raw = (payload.get("events") or {}).get("Events") or []
    return GameSnapshot(source=SnapshotSource.LIVE_CLIENT, game_time=float(game_data.get("gameTime", 0.0)), game_mode=str(game_data.get("gameMode", "UNKNOWN")), map_name=str(game_data.get("mapName", "UNKNOWN")), active_player_id=active_id, players=players, events=[_normalize_event(event) for event in events_raw])
