$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$analyticsDirectory = Join-Path $repositoryRoot "services\analytics"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv was not found. Install it with: winget install --id=astral-sh.uv -e"
}

Push-Location $analyticsDirectory

try {
    Write-Host "Preparing RiftPilot analytics..." -ForegroundColor Cyan
    uv sync --group dev

    Write-Host "Running automated checks..." -ForegroundColor Cyan
    uv run ruff check .
    uv run pytest

    Write-Host "Starting the local API..." -ForegroundColor Cyan
    $process = Start-Process `
        -FilePath "uv" `
        -ArgumentList @("run", "uvicorn", "riftpilot_analytics.main:app", "--host", "127.0.0.1", "--port", "8000") `
        -PassThru `
        -WindowStyle Hidden

    try {
        Start-Sleep -Seconds 2

        $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
        $liveGame = Invoke-RestMethod -Uri "http://127.0.0.1:8000/live-game/status"

        Write-Host ""
        Write-Host "RiftPilot service: $($health.status)" -ForegroundColor Green
        Write-Host "Live game status: $($liveGame.status)" -ForegroundColor Yellow

        if ($liveGame.status -eq "active") {
            Write-Host "League match detected." -ForegroundColor Green
            Write-Host "Level: $($liveGame.active_player.level)"
            Write-Host "Current gold: $($liveGame.active_player.currentGold)"
            Write-Host "Riot ID: $($liveGame.active_player.riotId)"
        }
        elseif ($liveGame.status -eq "inactive") {
            Write-Host "No active match detected. Start a Practice Tool match and run this script again."
        }
        else {
            Write-Host "The game API responded, but RiftPilot could not validate the response." -ForegroundColor Red
        }
    }
    finally {
        if ($null -ne $process -and -not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }
}
finally {
    Pop-Location
}
