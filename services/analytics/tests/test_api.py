from fastapi.testclient import TestClient

from riftpilot_analytics.api.dependencies import get_repository
from riftpilot_analytics.main import create_application
from riftpilot_analytics.storage.repository import SnapshotRepository


def make_client(tmp_path) -> TestClient:
    app = create_application()
    repository = SnapshotRepository(tmp_path / "api.db")
    app.dependency_overrides[get_repository] = lambda: repository
    return TestClient(app)


def test_health_and_demo_analysis(tmp_path) -> None:
    client = make_client(tmp_path)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    demo = client.post("/v1/demo/analyze?persist=true")
    assert demo.status_code == 200
    assert demo.json()["recommendations"]

    history = client.get("/v1/history")
    assert history.status_code == 200
    assert len(history.json()) == 1


def test_arbitrary_snapshot_analysis_and_simulation(tmp_path) -> None:
    client = make_client(tmp_path)
    snapshot = client.get("/v1/demo/snapshot").json()
    response = client.post("/v1/analyze?persist=true", json=snapshot)
    assert response.status_code == 200

    simulation = client.post(
        "/v1/simulate/defense",
        json={
            "health": 900,
            "armor": 50,
            "magic_resist": 40,
            "incoming_physical": 700,
            "incoming_magic": 500,
            "incoming_true": 100,
            "add_health": 250,
            "add_armor": 30,
            "add_magic_resist": 20,
        },
    )
    assert simulation.status_code == 200
    assert simulation.json()["survival_margin_gain"] > 0


def test_history_missing_returns_404(tmp_path) -> None:
    client = make_client(tmp_path)
    response = client.get("/v1/history/not-found")
    assert response.status_code == 404


def test_packaged_electron_origin_is_allowed(tmp_path) -> None:
    client = make_client(tmp_path)
    response = client.options(
        "/health",
        headers={
            "Origin": "null",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "null"
