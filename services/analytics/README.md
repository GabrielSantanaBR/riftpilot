# RiftPilot Analytics

Local Python service responsible for data collection, normalization, decision rules, and future statistical models.

## Current capability

- Starts a FastAPI application.
- Exposes a health endpoint.
- Validates its response with a Pydantic model.
- Includes automated tests and linting.

## Install dependencies

```powershell
uv sync --group dev
```

## Run quality checks

```powershell
uv run ruff check .
uv run pytest
```

## Start the service

```powershell
uv run uvicorn riftpilot_analytics.main:app --reload
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```
