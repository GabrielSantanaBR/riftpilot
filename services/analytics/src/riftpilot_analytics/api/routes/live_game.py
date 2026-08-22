"""Live game routes exposed to the desktop application."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from riftpilot_analytics.clients.live_client import (
    LiveClient,
    LiveClientResponseError,
    LiveClientUnavailableError,
)
from riftpilot_analytics.models.active_player import ActivePlayer

router = APIRouter(prefix="/live-game", tags=["live-game"])


class LiveGameStatusResponse(BaseModel):
    """Normalized live-game status returned to the desktop application."""

    status: Literal["active", "inactive", "error"]
    active_player: ActivePlayer | None = None
    message: str | None = None


@router.get("/status", response_model=LiveGameStatusResponse)
def get_live_game_status() -> LiveGameStatusResponse:
    """Detect a match and return supported local player data."""
    try:
        with LiveClient() as live_client:
            active_player = live_client.get_active_player()
    except LiveClientUnavailableError:
        return LiveGameStatusResponse(
            status="inactive",
            message="No active League of Legends match was detected.",
        )
    except LiveClientResponseError:
        return LiveGameStatusResponse(
            status="error",
            message="The League Live Client API returned an unexpected response.",
        )

    return LiveGameStatusResponse(status="active", active_player=active_player)
