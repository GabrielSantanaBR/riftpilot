"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from riftpilot_analytics import __version__
from riftpilot_analytics.api.routes.analysis import router as analysis_router
from riftpilot_analytics.api.routes.demo import router as demo_router
from riftpilot_analytics.api.routes.health import router as health_router
from riftpilot_analytics.api.routes.history import router as history_router
from riftpilot_analytics.api.routes.live import router as live_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="RiftPilot Analytics",
        description="Local-first League of Legends context analysis with explainable recommendations and counterfactual simulation.",
        version=__version__,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(analysis_router)
    application.include_router(live_router)
    application.include_router(demo_router)
    application.include_router(history_router)
    return application


app = create_application()
