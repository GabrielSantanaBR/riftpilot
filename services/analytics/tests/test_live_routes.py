from fastapi.testclient import TestClient

from riftpilot_analytics.api.dependencies import get_live_client, get_repository
from riftpilot_analytics.fixtures.demo import demo_snapshot
from riftpilot_analytics.ingestion.live_client import LiveClientUnavailable
from riftpilot_analytics.main import create_application
from riftpilot_analytics.storage.repository import SnapshotRepository


class FakeLiveClient:
    def __init__(self, available: bool = True) -> None:
        self.available = available

    async def get_all_game_data(self) -> dict[str, object]:
        if not self.available:
            raise LiveClientUnavailable("offline")
        return {"gameData": {"gameTime": 100}}

    async def get_snapshot(self):
        if not self.available:
            raise LiveClientUnavailable("offline")
        return demo_snapshot()


def make_client(
    tmp_path,
    *,
    available: bool = True,
) -> tuple[TestClient, SnapshotRepository]:
    app = create_application()
    repository = SnapshotRepository(tmp_path / "live.db")
    fake = FakeLiveClient(available=available)
    app.dependency_overrides[get_live_client] = lambda: fake
    app.dependency_overrides[get_repository] = lambda: repository
    return TestClient(app), repository


def test_live_status_reports_available(tmp_path) -> None:
    client, _ = make_client(tmp_path)
    response = client.get("/v1/live/status")
    assert response.status_code == 200
    assert response.json() == {"available": True, "source": "live_client"}


def test_live_status_reports_unavailable_without_error(tmp_path) -> None:
    client, _ = make_client(tmp_path, available=False)
    response = client.get("/v1/live/status")
    assert response.status_code == 200
    assert response.json() == {"available": False, "source": "live_client"}


def test_live_snapshot_returns_503_when_game_is_missing(tmp_path) -> None:
    client, _ = make_client(tmp_path, available=False)
    response = client.get("/v1/live/snapshot")
    assert response.status_code == 503
    assert "Start a match" in response.json()["detail"]


def test_live_analyze_returns_503_when_game_is_missing(tmp_path) -> None:
    client, _ = make_client(tmp_path, available=False)
    response = client.post("/v1/live/analyze")
    assert response.status_code == 503


def test_live_snapshot_and_analysis_share_the_pipeline(tmp_path) -> None:
    client, repository = make_client(tmp_path)
    snapshot_response = client.get("/v1/live/snapshot")
    assert snapshot_response.status_code == 200
    assert snapshot_response.json()["active_player_id"] == "RiftPilot Demo#BR1"

    analysis_response = client.post("/v1/live/analyze?persist=true")
    assert analysis_response.status_code == 200
    assert analysis_response.json()["recommendations"]
    assert len(repository.list_recent()) == 1
