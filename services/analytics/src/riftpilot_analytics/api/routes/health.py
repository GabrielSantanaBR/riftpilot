"""Health endpoint."""

from fastapi import APIRouter

from riftpilot_analytics import __version__

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "riftpilot-analytics", "version": __version__}
