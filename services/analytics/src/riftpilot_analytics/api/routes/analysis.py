"""Analysis and counterfactual endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from riftpilot_analytics.api.dependencies import get_engine, get_repository
from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.core.simulation import simulate_defense
from riftpilot_analytics.domain.models import (
    AnalysisResult,
    DefenseSimulationRequest,
    DefenseSimulationResult,
    GameSnapshot,
)
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1", tags=["analysis"])

EngineDependency = Annotated[DecisionEngine, Depends(get_engine)]
RepositoryDependency = Annotated[SnapshotRepository, Depends(get_repository)]


@router.post("/analyze", response_model=AnalysisResult)
def analyze_snapshot(
    snapshot: GameSnapshot,
    engine: EngineDependency,
    repository: RepositoryDependency,
    persist: bool = False,
) -> AnalysisResult:
    result = engine.analyze(snapshot)
    if persist:
        repository.save(snapshot, result)
    return result


@router.post("/simulate/defense", response_model=DefenseSimulationResult)
def defense_simulation(request: DefenseSimulationRequest) -> DefenseSimulationResult:
    return simulate_defense(request)
