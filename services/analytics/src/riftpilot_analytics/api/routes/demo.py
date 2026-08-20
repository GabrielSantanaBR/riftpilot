"""Portfolio-friendly deterministic demo endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from riftpilot_analytics.api.dependencies import get_engine, get_repository
from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.domain.models import AnalysisResult, GameSnapshot
from riftpilot_analytics.fixtures.demo import demo_snapshot
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/demo", tags=["demo"])

EngineDependency = Annotated[DecisionEngine, Depends(get_engine)]
RepositoryDependency = Annotated[SnapshotRepository, Depends(get_repository)]


@router.get("/snapshot", response_model=GameSnapshot)
def get_demo_snapshot() -> GameSnapshot:
    return demo_snapshot()


@router.post("/analyze", response_model=AnalysisResult)
def analyze_demo(
    engine: EngineDependency,
    repository: RepositoryDependency,
    persist: bool = False,
) -> AnalysisResult:
    snapshot = demo_snapshot()
    result = engine.analyze(snapshot)
    if persist:
        repository.save(snapshot, result)
    return result
