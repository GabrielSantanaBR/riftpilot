"""Local analysis history endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from riftpilot_analytics.api.dependencies import get_repository
from riftpilot_analytics.storage.repository import SnapshotRepository

router = APIRouter(prefix="/v1/history", tags=["history"])


@router.get("")
def list_history(limit: int = Query(default=20, ge=1, le=100), repository: SnapshotRepository = Depends(get_repository)) -> list[dict[str, Any]]:
    return repository.list_recent(limit)


@router.get("/{run_id}")
def get_history_run(run_id: str, repository: SnapshotRepository = Depends(get_repository)) -> dict[str, Any]:
    item = repository.get(run_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return item
