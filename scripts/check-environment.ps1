$ErrorActionPreference = "Stop"

$requiredNodeMajor = 24
$requiredPythonMajor = 3
$requiredPythonMinor = 13

function Get-CommandVersion {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        throw "Required command '$Command' was not found in PATH."
    }

    return (& $Command @Arguments 2>&1 | Select-Object -First 1).ToString().Trim()
}

function Get-RequiredPythonVersion {
    $candidates = @(
        @{
            Command = "python"
            Arguments = @("--version")
            Label = "python"
        },
        @{
            Command = "py"
            Arguments = @("-3.13", "--version")
            Label = "py -3.13"
        }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) {
            continue
        }

        $version = (
            & $candidate.Command @($candidate.Arguments) 2>&1 |
            Select-Object -First 1
        ).ToString().Trim()

        $match = [regex]::Match(
            $version,
            "^Python (?<major>\d+)\.(?<minor>\d+)\."
        )

        if (
            $match.Success -and
            [int]$match.Groups["major"].Value -eq $requiredPythonMajor -and
            [int]$match.Groups["minor"].Value -eq $requiredPythonMinor
        ) {
            return @{
                Version = $version
                Command = $candidate.Label
            }
        }
    }

    throw (
        "Python $requiredPythonMajor.$requiredPythonMinor.x was not found. " +
        "Install it and ensure either 'python' or 'py -3.13' can run it."
    )
}

Write-Host "Checking RiftPilot development environment..." -ForegroundColor Cyan

$gitVersion = Get-CommandVersion -Command "git" -Arguments @("--version")
$nodeVersion = Get-CommandVersion -Command "node" -Arguments @("--version")
$npmVersion = Get-CommandVersion -Command "npm" -Arguments @("--version")
$codeVersion = Get-CommandVersion -Command "code" -Arguments @("--version")
$python = Get-RequiredPythonVersion

$nodeMatch = [regex]::Match($nodeVersion, "^v(?<major>\d+)\.")
if (-not $nodeMatch.Success) {
    throw "Could not parse Node.js version: $nodeVersion"
}

$nodeMajor = [int]$nodeMatch.Groups["major"].Value

if ($nodeMajor -ne $requiredNodeMajor) {
    throw "Node.js $requiredNodeMajor.x is required, but '$nodeVersion' is installed."
}

Write-Host ""
Write-Host "Environment is ready." -ForegroundColor Green
Write-Host "  $gitVersion"
Write-Host "  Node.js $nodeVersion"
Write-Host "  npm $npmVersion"
Write-Host "  $($python.Version) through '$($python.Command)'"
Write-Host "  VS Code $codeVersion"
