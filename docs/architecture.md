# Architecture

## Design goals

1. Keep game integration read-only and local.
2. Separate Riot's external payload shape from RiftPilot's domain model.
3. Make every recommendation auditable.
4. Degrade confidence when data is missing instead of fabricating certainty.
5. Make the complete product reviewable without a running League match.
6. Keep the first analytical baseline deterministic so future ML can be evaluated against it.

## Components

### LiveClientClient
Owns the only direct connection to the League game client. It reads `/liveclientdata/allgamedata` from the local HTTPS endpoint and converts transport failures into a domain-specific `LiveClientUnavailable` error.

### Normalizer
Maps unstable/external field names into stable Pydantic models. RiotID aliases and missing fields are handled at this boundary.

### Feature engineering
Computes compact contextual features such as health ratio, CS/min, level delta, team kill delta, recent combat, survival risk, tempo, economy pressure, and data completeness.

The scores are **context indicators**, not hidden win probabilities.

### Decision engine
Consumes only normalized features and returns versioned recommendations. Rules are explicit and testable. Confidence is multiplied by data completeness.

### Counterfactual simulator
Allows direct comparison of defensive-stat scenarios. It is separate from recommendations so the user can ask "what if" questions without pretending the simulator knows future incoming damage.

### SQLite repository
Optional local persistence stores both the input snapshot and exact analysis output. This gives reproducibility: an old recommendation can be inspected even after the engine changes.

### Desktop client
Electron hosts a React/Vite renderer. The renderer talks only to the local FastAPI service and defaults to a deterministic demo mode for portfolio review.

## Model evolution strategy

The deterministic engine is the baseline. A statistical model should not replace it until the project has:

- a labeled outcome definition;
- a leakage-safe feature set;
- train/validation/test time splits;
- calibration analysis;
- comparison against the deterministic baseline;
- recorded model version and feature schema.

This prevents "AI" from becoming an untestable marketing label.
