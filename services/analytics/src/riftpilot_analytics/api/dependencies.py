"""Application-level dependencies."""

import os
from functools import lru_cache
from pathlib import Path

from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.ingestion.live_client import LiveClientClient
from riftpilot_analytics.storage.repository import SnapshotRepository


@lru_cache
def get_engine() -> DecisionEngine:
    return DecisionEngine()


@lru_cache
def get_live_client() -> LiveClientClient:
    return LiveClientClient()


@lru_cache
def get_repository() -> SnapshotRepository:
    path = Path(os.getenv("RIFTPILOT_DB_PATH", ".riftpilot/riftpilot.db"))
    return SnapshotRepository(path)
