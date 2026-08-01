# ADR 0004: Python Service Tooling

- **Status:** Accepted
- **Date:** 2026-08-01

## Context

The analytics service needs reproducible dependency installation, isolated environments, automated tests, and consistent code quality checks.

Using separate commands for virtual environments, package installation, and lock files would add unnecessary setup work.

## Decision

Use:

- `uv` for Python dependency management, virtual environments, command execution, and lock files.
- `pyproject.toml` as the source of project metadata and tool configuration.
- FastAPI for the local HTTP interface.
- Pydantic response models for API data validation.
- pytest and HTTPX through FastAPI's `TestClient` for automated API tests.
- Ruff for linting and import organization.
- A `src` package layout to prevent accidental imports from the repository directory.

The analytics service will be isolated inside `services/analytics`.

## Consequences

### Positive

- One tool manages the environment, dependencies, lock file, and commands.
- Tests run without manually activating the virtual environment.
- Dependencies can be reproduced from `uv.lock`.
- The service has a clear package boundary.
- The future desktop application can communicate with a stable local API.

### Negative

- Contributors must install `uv`.
- The Electron packaging process will eventually need to start and stop a Python process.
- A local HTTP interface requires explicit error handling and port management.
