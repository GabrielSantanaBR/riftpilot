"""Domain models shared by ingestion, analysis, persistence, and the API."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, computed_field


class Team(StrEnum):
    ORDER = "ORDER"
    CHAOS = "CHAOS"
    UNKNOWN = "UNKNOWN"


class SnapshotSource(StrEnum):
    LIVE_CLIENT = "live_client"
    DEMO = "demo"
    API = "api"


class Score(BaseModel):
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    creep_score: int = 0
    ward_score: float = 0.0

    @computed_field
    @property
    def kda(self) -> float:
        return round((self.kills + self.assists) / max(self.deaths, 1), 2)


class ItemState(BaseModel):
    item_id: int = 0
    name: str = "Unknown item"
    count: int = 1
    price: int = 0


class ChampionStats(BaseModel):
    current_health: float = 0.0
    max_health: float = 0.0
    armor: float = 0.0
    magic_resist: float = 0.0
    attack_damage: float = 0.0
    ability_power: float = 0.0
    move_speed: float = 0.0
    ability_haste: float = 0.0

    @computed_field
    @property
    def health_ratio(self) -> float:
        if self.max_health <= 0:
            return 1.0
        return round(max(0.0, min(1.0, self.current_health / self.max_health)), 4)


class PlayerState(BaseModel):
    riot_id: str
    champion_name: str
    team: Team = Team.UNKNOWN
    level: int = 1
    is_active: bool = False
    score: Score = Field(default_factory=Score)
    items: list[ItemState] = Field(default_factory=list)
    stats: ChampionStats | None = None
    current_gold: float | None = None


class GameEvent(BaseModel):
    event_id: int | None = None
    event_name: str
    event_time: float
    actor: str | None = None
    victim: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class GameSnapshot(BaseModel):
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source: SnapshotSource = SnapshotSource.API
    game_time: float = 0.0
    game_mode: str = "UNKNOWN"
    map_name: str = "UNKNOWN"
    active_player_id: str
    players: list[PlayerState]
    events: list[GameEvent] = Field(default_factory=list)

    def active_player(self) -> PlayerState:
        for player in self.players:
            if player.is_active or player.riot_id == self.active_player_id:
                return player
        raise ValueError("Active player not found in snapshot")

    def enemies_of(self, player: PlayerState) -> list[PlayerState]:
        if player.team == Team.UNKNOWN:
            return [p for p in self.players if p.riot_id != player.riot_id]
        return [p for p in self.players if p.team not in {player.team, Team.UNKNOWN}]

    def allies_of(self, player: PlayerState) -> list[PlayerState]:
        return [p for p in self.players if p.team == player.team and p.riot_id != player.riot_id]


class DecisionSignal(BaseModel):
    key: str
    label: str
    value: float
    normalized: float = Field(ge=0.0, le=1.0)
    interpretation: str


class ContextFeatures(BaseModel):
    cs_per_minute: float
    kda: float
    health_ratio: float
    level_delta: float
    team_kill_delta: int
    current_gold: float | None
    recent_deaths: int
    recent_kills: int
    survival_risk: float = Field(ge=0.0, le=1.0)
    tempo_score: float = Field(ge=0.0, le=1.0)
    economy_pressure: float = Field(ge=0.0, le=1.0)
    data_completeness: float = Field(ge=0.0, le=1.0)
    signals: list[DecisionSignal]


class RecommendationCategory(StrEnum):
    SURVIVAL = "survival"
    ECONOMY = "economy"
    TEMPO = "tempo"
    VISION = "vision"
    FARM = "farm"
    BUILD = "build"


class Recommendation(BaseModel):
    id: str
    category: RecommendationCategory
    title: str
    priority: int = Field(ge=1, le=100)
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    reasons: list[str]
    evidence: dict[str, float | int | str | None]
    counterfactual: str


class AnalysisResult(BaseModel):
    engine_version: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    active_player_id: str
    features: ContextFeatures
    recommendations: list[Recommendation]
    state_fingerprint: str


class DefenseSimulationRequest(BaseModel):
    health: float = Field(gt=0)
    armor: float
    magic_resist: float
    incoming_physical: float = Field(ge=0)
    incoming_magic: float = Field(ge=0)
    incoming_true: float = Field(ge=0)
    add_health: float = Field(default=0, ge=0)
    add_armor: float = 0
    add_magic_resist: float = 0


class DefenseScenario(BaseModel):
    effective_damage: float
    remaining_health: float
    survives: bool
    survival_margin: float


class DefenseSimulationResult(BaseModel):
    baseline: DefenseScenario
    upgraded: DefenseScenario
    damage_reduction_gain: float
    survival_margin_gain: float
    verdict: str
