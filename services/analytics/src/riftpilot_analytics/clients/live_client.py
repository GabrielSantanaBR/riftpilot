"""Client for the League of Legends Live Client Data API."""

import httpx
from pydantic import ValidationError

from riftpilot_analytics.models.active_player import ActivePlayer

LIVE_CLIENT_BASE_URL = "https://127.0.0.1:2999"
ACTIVE_PLAYER_PATH = "/liveclientdata/activeplayer"
DEFAULT_TIMEOUT_SECONDS = 2.0


class LiveClientUnavailableError(Exception):
    """Raised when no active League of Legends match can be reached."""


class LiveClientResponseError(Exception):
    """Raised when the local game API returns an unexpected response."""


class LiveClient:
    """Read supported data exposed locally by the running game."""

    def __init__(
        self,
        base_url: str = LIVE_CLIENT_BASE_URL,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout_seconds,
            verify=False,
            transport=transport,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "LiveClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def get_active_player(self) -> ActivePlayer:
        """Read and validate the local player's live data."""
        try:
            response = self._client.get(ACTIVE_PLAYER_PATH)
            response.raise_for_status()
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as error:
            raise LiveClientUnavailableError(
                "No active League of Legends match could be reached."
            ) from error
        except httpx.HTTPError as error:
            raise LiveClientResponseError(
                "The League Live Client API returned an HTTP error."
            ) from error

        try:
            return ActivePlayer.model_validate(response.json())
        except (ValueError, ValidationError) as error:
            raise LiveClientResponseError(
                "The League Live Client API returned invalid active-player data."
            ) from error
