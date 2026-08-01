"""Service health endpoint."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from riftpilot_analytics import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response returned when the analytics service is available."""

    status: Literal["ok"]
    service: str
    version: str


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Return the current service status."""

    return HealthResponse(
        status="ok",
        service="riftpilot-analytics",
        version=__version__,
    )
