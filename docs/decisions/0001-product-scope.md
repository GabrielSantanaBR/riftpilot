# ADR 0001 — Product Scope

## Status

Accepted

## Context

RiftPilot started from the idea of a desktop assistant that interprets League of Legends match context and helps the player reason about builds, matchups, objectives and rotations.

The idea can easily become too broad or cross fair-play boundaries if hidden information, automated inputs or unsupported client access are treated as product requirements.

## Decision

RiftPilot is an analytics and decision-support project. It may process only information available to the player through allowed local/public sources and historical datasets.

The product can recommend and explain. It must not play the game for the user.

Initial scope:

- match context representation;
- matchup analysis;
- conditional build recommendations;
- objective/rotation heuristics;
- post-match analytics;
- historical/statistical experimentation.

## Consequences

The project prioritizes explainable analytics and domain modeling before UI polish or machine learning. Data-source decisions must be reviewed against this scope.