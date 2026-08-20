#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../services/analytics"
uv sync --group dev
uv run uvicorn riftpilot_analytics.main:app --reload
