"""FastAPI application entry point."""

from fastapi import FastAPI

from riftpilot_analytics import __version__
from riftpilot_analytics.api.routes.health import router as health_router


def create_application() -> FastAPI:
    """Create and configure the local analytics API."""

    application = FastAPI(
        title="RiftPilot Analytics",
        description="Local analytics and decision-support service.",
        version=__version__,
    )
    application.include_router(health_router)

    return application


app = create_application()
