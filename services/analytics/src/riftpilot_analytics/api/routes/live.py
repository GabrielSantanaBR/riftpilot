"""Endpoints that read only from the local League Live Client Data API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from riftpilot_analytics.api.dependencies import get_engine, get_live_client, get_repository
from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.domain.models import AnalysisResult, GameSnapshot
from riftpilot_analytics.ingestion.live_client import LiveClientClient, LiveClientUnavailable
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/live", tags=["live"])

ClientDependency = Annotated[LiveClientClient, Depends(get_live_client)]
EngineDependency = Annotated[DecisionEngine, Depends(get_engine)]
RepositoryDependency = Annotated[SnapshotRepository, Depends(get_repository)]


@router.get("/status")
async def live_status(client: ClientDependency) -> dict[str, bool | str]:
    try:
        await client.get_all_game_data()
        return {"available": True, "source": "live_client"}
    except LiveClientUnavailable:
        return {"available": False, "source": "live_client"}


@router.get("/snapshot", response_model=GameSnapshot)
async def live_snapshot(client: ClientDependency) -> GameSnapshot:
    try:
        return await client.get_snapshot()
    except LiveClientUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="League live client is not available. Start a match or use demo mode.",
        ) from exc


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_live(
    client: ClientDependency,
    engine: EngineDependency,
    repository: RepositoryDependency,
    persist: bool = True,
) -> AnalysisResult:
    try:
        snapshot = await client.get_snapshot()
    except LiveClientUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="League live client is not available. Start a match or use demo mode.",
        ) from exc
    result = engine.analyze(snapshot)
    if persist:
        repository.save(snapshot, result)
    return result
