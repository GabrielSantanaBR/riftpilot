# Riot / League integration boundaries

This document is an engineering checklist, not legal advice.

## Current integration

RiftPilot uses the local League **Live Client Data API** documented by Riot for native applications. The service reads match data over localhost and keeps analysis local by default.

## Hard product boundaries

RiftPilot must not:

- read process memory;
- inject or modify the game client;
- automate player input;
- reconstruct hidden/fog-of-war information;
- include a Riot API key inside a distributed desktop binary;
- imply official Riot affiliation.

## Before public distribution

Riot's current developer policy states that player-facing products must be registered/audited through the Developer Portal, and products that use League Client APIs should disclose those endpoints/use cases during registration.

Before shipping a public build:

1. Register the product in the Riot Developer Portal.
2. Re-check current General and League-specific policies.
3. Add Riot's required legal boilerplate exactly as specified by the then-current policy.
4. Document every Riot/League endpoint used.
5. Keep any future production API key server-side; never bundle it in Electron.
6. Re-audit the app whenever a new integration or monetized feature is introduced.

## Privacy posture

The default architecture requires no cloud account. Match snapshots and history are stored locally in SQLite only when persistence is enabled. A future sync feature should be opt-in, disclose retention, and minimize player-identifying data.
