"""Portfolio-friendly deterministic demo endpoints."""

from fastapi import APIRouter, Depends

from riftpilot_analytics.api.dependencies import get_engine, get_repository
from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.domain.models import AnalysisResult, GameSnapshot
from riftpilot_analytics.fixtures.demo import demo_snapshot
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/demo", tags=["demo"])


@router.get("/snapshot", response_model=GameSnapshot)
def get_demo_snapshot() -> GameSnapshot:
    return demo_snapshot()


@router.post("/analyze", response_model=AnalysisResult)
def analyze_demo(persist: bool = False, engine: DecisionEngine = Depends(get_engine), repository: SnapshotRepository = Depends(get_repository)) -> AnalysisResult:
    snapshot = demo_snapshot()
    result = engine.analyze(snapshot)
    if persist:
        repository.save(snapshot, result)
    return result
