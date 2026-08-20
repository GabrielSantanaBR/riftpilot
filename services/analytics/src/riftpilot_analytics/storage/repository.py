"""Local SQLite persistence for snapshots and explainable decisions."""

from __future__ import annotations

import json
import sqlite3
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from riftpilot_analytics.domain.models import AnalysisResult, GameSnapshot


class SnapshotRepository:
    def __init__(self, database_path: str | Path = "riftpilot.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS analysis_runs (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    active_player_id TEXT NOT NULL,
                    state_fingerprint TEXT NOT NULL,
                    snapshot_json TEXT NOT NULL,
                    analysis_json TEXT NOT NULL
                )
            """)
            connection.execute("CREATE INDEX IF NOT EXISTS idx_analysis_runs_created_at ON analysis_runs(created_at DESC)")

    def save(self, snapshot: GameSnapshot, analysis: AnalysisResult) -> str:
        run_id = str(uuid.uuid4())
        with self._connection() as connection:
            connection.execute("""
                INSERT INTO analysis_runs (
                    id, created_at, source, active_player_id, state_fingerprint,
                    snapshot_json, analysis_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (run_id, datetime.now(UTC).isoformat(), snapshot.source.value, snapshot.active_player_id, analysis.state_fingerprint, snapshot.model_dump_json(), analysis.model_dump_json()))
        return run_id

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 100))
        with self._connection() as connection:
            rows = connection.execute("""
                SELECT id, created_at, source, active_player_id, state_fingerprint, analysis_json
                FROM analysis_runs
                ORDER BY created_at DESC
                LIMIT ?
            """, (safe_limit,)).fetchall()
        return [{"id": row["id"], "created_at": row["created_at"], "source": row["source"], "active_player_id": row["active_player_id"], "state_fingerprint": row["state_fingerprint"], "analysis": json.loads(row["analysis_json"])} for row in rows]

    def get(self, run_id: str) -> dict[str, Any] | None:
        with self._connection() as connection:
            row = connection.execute("SELECT * FROM analysis_runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            return None
        return {"id": row["id"], "created_at": row["created_at"], "source": row["source"], "active_player_id": row["active_player_id"], "state_fingerprint": row["state_fingerprint"], "snapshot": json.loads(row["snapshot_json"]), "analysis": json.loads(row["analysis_json"])}
