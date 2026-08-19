# ADR 0003 — Data and Fair Play

## Status

Accepted

## Context

A real-time game assistant must distinguish useful analytics from access to information the player should not have. The project also needs a stable rule for deciding whether a future data source is acceptable.

## Decision

RiftPilot will only consume data that is legitimately available to the player or provided by approved/public interfaces and datasets.

The system must not:

- infer or expose hidden enemy information as factual live state;
- automate gameplay inputs;
- alter the game client;
- bypass access restrictions;
- present uncertain inferred information as directly observed data.

Every adapter must identify its source and whether fields are live, historical, static or inferred.

## Consequences

The domain model should preserve data provenance. Recommendation explanations can distinguish observed facts from statistical estimates. New integrations require a source review before implementation.