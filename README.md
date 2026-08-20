# RiftPilot

**RiftPilot is a local-first, explainable match-intelligence desktop application for League of Legends.** It converts data that the player is already allowed to see into an explicit decision trace: what matters now, how confident the system is, which signals caused the recommendation, and what would change under a counterfactual scenario.

The project is intentionally designed as a serious **Data + Backend + Desktop Product** portfolio piece rather than an overlay that pretends to be an opaque "AI coach".

## Why this project exists

Most game-assistant demos stop at static build lists. RiftPilot focuses on a harder engineering problem: **turning noisy live context into safe, explainable, testable decisions without reading hidden information or automating gameplay.**

The system demonstrates:

- real-time-ish local data ingestion;
- domain normalization over an external API shape;
- feature engineering and deterministic decision scoring;
- uncertainty-aware recommendations;
- counterfactual simulation;
- SQLite event/history persistence;
- FastAPI/OpenAPI design;
- Electron + React + TypeScript desktop UX;
- automated backend tests and CI;
- compliance-conscious product architecture.

## Product flow

```text
League Live Client Data API                 Deterministic Demo Fixture
       (localhost:2999)                              │
               │                                     │
               └─────────────┬───────────────────────┘
                             ▼
                     Snapshot Normalizer
                             ▼
                      Domain Match State
                             ▼
                     Feature Engineering
                             ▼
             Explainable Decision Engine v0.4
                  │                    │
                  ▼                    ▼
        Recommendations         Counterfactual Lab
                  │                    │
                  └──────────┬─────────┘
                             ▼
                 FastAPI + local SQLite history
                             ▼
                Electron / React desktop client
```

## What makes RiftPilot different

### Decision Trace
Every recommendation contains a priority, confidence score, plain-language reasons, structured evidence, and a counterfactual describing which state change would make the advice disappear or flip.

### Uncertainty-aware confidence
Confidence is reduced when useful fields are unavailable. A missing live field does not silently become fake certainty.

### Replayable Demo Mode
A reviewer can inspect the full flow without owning League or starting a match. The same engine analyzes a deterministic fixture exposed at `/v1/demo/*`.

### Counterfactual Defense Lab
The `/v1/simulate/defense` endpoint compares baseline and upgraded defensive stats against a supplied physical/magic/true damage packet. It uses League-style resistance math and reports whether the stat change flips a lethal scenario.

### Local-first history
Snapshots and analysis results can be stored in SQLite on the user's machine. The default design does not require uploading live match state to a remote server.

## Repository structure

```text
riftpilot/
├── apps/
│   └── desktop/                 # Electron + React + TypeScript client
├── services/
│   └── analytics/               # FastAPI analytics service
│       ├── src/riftpilot_analytics/
│       │   ├── api/             # HTTP routes and dependencies
│       │   ├── core/            # features, engine, simulation
│       │   ├── domain/          # stable Pydantic domain models
│       │   ├── fixtures/        # deterministic demo match
│       │   ├── ingestion/       # Live Client Data API adapter
│       │   └── storage/         # SQLite repository
│       └── tests/
├── docs/                        # architecture, demo, compliance
├── scripts/
└── .github/workflows/
```

## Run the analytics service

Requirements: Python 3.13 and `uv`.

```bash
cd services/analytics
uv sync --group dev
uv run ruff check .
uv run pytest
uv run uvicorn riftpilot_analytics.main:app --reload
```

OpenAPI: `http://127.0.0.1:8000/docs`

### Fast demo

```bash
curl -X POST http://127.0.0.1:8000/v1/demo/analyze
```

## Run the desktop client

Requirements: Node.js 22+.

```bash
cd apps/desktop
npm install
npm run desktop:dev
```

Keep the analytics service running on `127.0.0.1:8000`.

## Main API endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Service health/version |
| `GET /v1/live/status` | Checks whether the local game endpoint is available |
| `GET /v1/live/snapshot` | Normalized live match state |
| `POST /v1/live/analyze` | Analyze current live state and optionally persist it |
| `GET /v1/demo/snapshot` | Deterministic reviewer fixture |
| `POST /v1/demo/analyze` | Full analysis without League running |
| `POST /v1/analyze` | Analyze any valid normalized snapshot |
| `POST /v1/simulate/defense` | Counterfactual survivability comparison |
| `GET /v1/history` | Local analysis history |
| `GET /v1/history/{id}` | Full stored snapshot + decision trace |

## Engineering boundaries

RiftPilot is deliberately read-only. It does **not**:

- read League process memory;
- inject code or modify the game/client;
- automate inputs or gameplay;
- attempt to recover fog-of-war or other hidden information;
- claim a heuristic score is a trained ML model.

The current decision engine is deterministic and versioned. That choice makes it testable and provides a clean baseline for future statistical models. A future ML layer should only be promoted after a real labeled dataset and out-of-sample evaluation exist.

## Portfolio narrative

A useful way to present RiftPilot in an interview:

> I built a local decision-support system around a live external API. The hard part was not calling the endpoint; it was defining a stable domain model, handling partial data, creating explainable features, versioning decision logic, preserving privacy, and building a demo that anyone can reproduce without the original game environment.

See `docs/architecture.md` for deeper technical rationale and `docs/compliance.md` for Riot-specific product constraints.

## Status

**v0.4 portfolio release:** analytics engine, live normalization, demo mode, decision trace, counterfactual simulator, SQLite history, API, desktop dashboard, tests, and CI are implemented.

Future work is intentionally evidence-driven: patch-aware static-data enrichment, labeled outcome collection, calibration metrics, and only then statistical/ML models.

## Legal

RiftPilot is an independent portfolio project and is not endorsed by Riot Games. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. See `docs/compliance.md` before distributing the application to players.
