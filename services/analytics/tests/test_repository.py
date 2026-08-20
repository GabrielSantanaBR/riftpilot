from riftpilot_analytics.core.engine import DecisionEngine
from riftpilot_analytics.fixtures.demo import demo_snapshot
from riftpilot_analytics.storage.repository import SnapshotRepository


def test_repository_roundtrip(tmp_path) -> None:
    repository = SnapshotRepository(tmp_path / "history.db")
    snapshot = demo_snapshot()
    analysis = DecisionEngine().analyze(snapshot)
    run_id = repository.save(snapshot, analysis)
    recent = repository.list_recent(10)
    assert recent[0]["id"] == run_id
    assert recent[0]["analysis"]["state_fingerprint"] == analysis.state_fingerprint
    item = repository.get(run_id)
    assert item is not None
    assert item["snapshot"]["active_player_id"] == snapshot.active_player_id
    assert repository.get("missing") is None
