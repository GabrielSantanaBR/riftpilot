"""Endpoints that read only from the local League Live Client Data API."""

from fastapi import APIRouter, Depends, HTTPException, status

from riftpilot_analytics.api.dependencies import get_engine, get_live_client, get_repository
from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.domain.models import AnalysisResult, GameSnapshot
from riftpilot_analytics.ingestion.live_client import LiveClientClient, LiveClientUnavailable
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/live", tags=["live"])


@router.get("/status")
async def live_status(client: LiveClientClient = Depends(get_live_client)) -> dict[str, bool | str]:
    try:
        await client.get_all_game_data()
        return {"available": True, "source": "live_client"}
    except LiveClientUnavailable:
        return {"available": False, "source": "live_client"}


@router.get("/snapshot", response_model=GameSnapshot)
async def live_snapshot(client: LiveClientClient = Depends(get_live_client)) -> GameSnapshot:
    try:
        return await client.get_snapshot()
    except LiveClientUnavailable as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="League live client is not available. Start a match or use demo mode.") from exc


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_live(persist: bool = True, client: LiveClientClient = Depends(get_live_client), engine: DecisionEngine = Depends(get_engine), repository: SnapshotRepository = Depends(get_repository)) -> AnalysisResult:
    try:
        snapshot = await client.get_snapshot()
    except LiveClientUnavailable as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="League live client is not available. Start a match or use demo mode.") from exc
    result = engine.analyze(snapshot)
    if persist:
        repository.save(snapshot, result)
    return result
