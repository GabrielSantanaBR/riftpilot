# Reviewer demo

The goal of Demo Mode is to make RiftPilot testable in under five minutes without League installed.

## API-only demo

1. Start `services/analytics`.
2. Open `/docs`.
3. Execute `POST /v1/demo/analyze`.
4. Inspect `features`, ordered `recommendations`, `evidence`, and `counterfactual`.
5. Execute `POST /v1/simulate/defense` with a lethal baseline and added health/resistance.
6. Run demo analysis with `persist=true`, then inspect `/v1/history`.

## Desktop demo

1. Start the analytics API.
2. Start `apps/desktop` with `npm run desktop:dev`.
3. Keep **Demo** selected.
4. Review the decision window, contextual metrics, recommendation stack, scoreboard, and combat trace.
5. Switch to **Live** to demonstrate graceful handling when the League endpoint is unavailable.

## Interview points

- External API normalization is isolated from business logic.
- Scores are labeled as context indicators, not fake win probabilities.
- Missing data reduces confidence.
- The same domain model supports live, demo, API, persistence, and tests.
- Stored analyses include a state fingerprint for reproducibility.
