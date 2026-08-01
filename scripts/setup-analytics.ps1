$ErrorActionPreference = "Stop"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv was not found. Install it with: winget install --id=astral-sh.uv -e"
}

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$analyticsDirectory = Join-Path $repositoryRoot "services\analytics"

if (-not (Test-Path $analyticsDirectory)) {
    throw "Analytics service directory was not found: $analyticsDirectory"
}

Push-Location $analyticsDirectory

try {
    Write-Host "Installing analytics dependencies..." -ForegroundColor Cyan
    uv sync --group dev

    Write-Host ""
    Write-Host "Running Ruff..." -ForegroundColor Cyan
    uv run ruff check .

    Write-Host ""
    Write-Host "Running tests..." -ForegroundColor Cyan
    uv run pytest

    Write-Host ""
    Write-Host "Analytics service is ready." -ForegroundColor Green
}
finally {
    Pop-Location
}
