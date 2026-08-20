"""Local analysis history endpoints."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query

from riftpilot_analytics.api.dependencies import get_repository
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/history", tags=["history"])

RepositoryDependency = Annotated[SnapshotRepository, Depends(get_repository)]
HistoryLimit = Annotated[int, Query(ge=1, le=100)]


@router.get("")
def list_history(
    repository: RepositoryDependency,
    limit: HistoryLimit = 20,
) -> list[dict[str, Any]]:
    return repository.list_recent(limit)


@router.get("/{run_id}")
def get_history_run(
    run_id: str,
    repository: RepositoryDependency,
) -> dict[str, Any]:
    item = repository.get(run_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return item
