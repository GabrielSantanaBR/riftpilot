# RiftPilot Analytics

Local FastAPI service that converts Riot Live Client Data API snapshots into a stable domain model, extracts contextual signals, emits explainable recommendations, runs defensive counterfactual simulations, and stores optional local history in SQLite.

## Run

```bash
uv sync --group dev
uv run uvicorn riftpilot_analytics.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.

## Demo without League

```bash
curl -X POST http://127.0.0.1:8000/v1/demo/analyze
```

No Riot API key is required for the Live Client Data API because it is served locally by an active game client. RiftPilot does not read process memory, inject code, automate gameplay, or attempt to expose hidden information.
