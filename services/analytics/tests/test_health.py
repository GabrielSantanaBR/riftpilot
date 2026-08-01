"""Tests for the service health endpoint."""

from fastapi.testclient import TestClient

from riftpilot_analytics import __version__
from riftpilot_analytics.main import app

client = TestClient(app)


def test_health_endpoint_returns_service_information() -> None:
    """The health endpoint should confirm that the service is available."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "riftpilot-analytics",
        "version": __version__,
    }
