# RiftPilot Roadmap

## Phase 0 — Foundation

- [x] Monorepo structure
- [x] Analytics service
- [x] FastAPI health endpoint
- [x] Ruff
- [x] Pytest
- [x] Coverage threshold
- [x] Development setup
- [x] Product and architecture documentation

## Phase 1 — Domain and data foundation

Goal: represent match context reliably before making recommendations.

- [ ] Champion model
- [ ] Item model
- [ ] Player/champion state
- [ ] Team composition model
- [ ] Objective state
- [ ] Match timeline/event model
- [ ] Patch/version metadata
- [ ] Data source adapters
- [ ] Normalization layer
- [ ] Fixture datasets for tests

Deliverable: given an allowed raw payload, produce a normalized `MatchState`.

## Phase 2 — Explainable decision engine

Goal: generate deterministic recommendations that can be inspected and tested.

- [ ] Rule interface
- [ ] Recommendation schema
- [ ] Confidence/priority score
- [ ] Human-readable explanation
- [ ] Matchup heuristics
- [ ] Conditional item/build rules
- [ ] Objective timing rules
- [ ] Rotation opportunity rules
- [ ] Unit tests for every rule family

Deliverable: `MatchState -> Recommendation[]`.

## Phase 3 — Historical analytics

- [ ] Local persistence
- [ ] Match ingestion pipeline
- [ ] Feature engineering
- [ ] Performance metrics
- [ ] Player tendency summaries
- [ ] Recommendation outcome tracking
- [ ] Post-match report

Deliverable: local historical dataset and reproducible analytics reports.

## Phase 4 — Statistical models

Machine learning only enters after enough validated historical data exists.

Candidate experiments:

- matchup difficulty estimation;
- win-probability calibration by game state;
- item effectiveness conditioned on context;
- objective contest risk;
- clustering of player/game patterns.

Every model must be compared against a simple baseline and expose evaluation metrics.

## Phase 5 — Desktop application

- [ ] Desktop shell technology decision
- [ ] Local service lifecycle
- [ ] Match dashboard
- [ ] Recommendation feed
- [ ] Build view
- [ ] Matchup view
- [ ] Post-match analytics
- [ ] Settings and privacy controls

## Phase 6 — Product hardening

- [ ] CI pipeline
- [ ] Structured logging
- [ ] Versioned API contracts
- [ ] Database migrations
- [ ] Packaging/installer
- [ ] Performance profiling
- [ ] Security review
- [ ] Fair-play/source compliance review

## Non-goals

RiftPilot will not be designed to reveal hidden enemy information, automate gameplay, send automated inputs to the game, or bypass platform restrictions.
