$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot/../services/analytics"
uv sync --group dev
uv run uvicorn riftpilot_analytics.main:app --reload
