"""Validated models for locally available live game data."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ActivePlayer(BaseModel):
    """Small, stable subset of the active-player payload."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    current_gold: float = Field(alias="currentGold")
    level: int
    riot_id: str | None = Field(default=None, alias="riotId")
    riot_id_game_name: str | None = Field(default=None, alias="riotIdGameName")
    riot_id_tag_line: str | None = Field(default=None, alias="riotIdTagLine")
    champion_stats: dict[str, Any] = Field(default_factory=dict, alias="championStats")
