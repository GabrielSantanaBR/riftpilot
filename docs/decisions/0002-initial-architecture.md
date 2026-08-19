# ADR 0002 — Initial Architecture

## Status

Accepted

## Context

RiftPilot needs to combine data ingestion, normalization, business rules, analytics and eventually a desktop interface. Keeping all responsibilities inside one application would make testing and experimentation harder.

## Decision

Use a modular architecture with a local analytics service as the first independently testable component.

Planned flow:

```text
allowed data sources -> adapters -> normalization -> MatchState
                                             |
                                             +-> rule engine
                                             +-> statistical models
                                                       |
                                                       v
                                                recommendations
                                                       |
                                                       v
                                                desktop client
```

The Python analytics service owns the analytical domain. The future desktop client owns presentation and local user interaction.

## Consequences

- Domain logic can be tested without a UI.
- Data-source adapters can change without rewriting recommendations.
- The desktop technology can be chosen later.
- API contracts between desktop and analytics must eventually be versioned.