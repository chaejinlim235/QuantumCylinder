param(
    [string]$RepoDir = "C:\Coding\Hackathon\2026Quantum",
    [string]$RepoUrl = "https://github.com/chaejinlim235/QuantumCylinder.git",
    [string]$WorkerName = "seungbin",
    [switch]$SetupEnv,
    [switch]$KeepDisplayOff,
    [switch]$Detached
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Assert-LastExitCode {
    param([string]$CommandName)

    if ($LASTEXITCODE -ne 0) {
        throw "$CommandName failed with exit code $LASTEXITCODE"
    }
}

function Get-PythonForRepo {
    param([string]$RepoRoot)

    $venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPython) {
        return $venvPython
    }

    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    throw "Could not find python. Install Python 3.11+ first."
}

if (-not (Test-Path -LiteralPath $RepoDir)) {
    $parent = Split-Path -Parent $RepoDir
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Write-Step "Cloning repository into $RepoDir"
    git clone $RepoUrl $RepoDir
    Assert-LastExitCode "git clone"
}

Push-Location $RepoDir
try {
    Write-Step "Repository: $RepoDir"
    git fetch --prune origin
    Assert-LastExitCode "git fetch --prune origin"

    $branch = (git branch --show-current).Trim()
    $trackedChanges = @(git status --porcelain --untracked-files=no | Where-Object { $_ })
    if ($branch -eq "main" -and $trackedChanges.Count -eq 0) {
        git pull --ff-only origin main
        Assert-LastExitCode "git pull --ff-only origin main"
    }
    else {
        Write-Step "Pull skipped because branch is '$branch' or tracked local changes exist."
    }

    $venvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"
    if ($SetupEnv -or -not (Test-Path -LiteralPath $venvPython)) {
        Write-Step "Preparing local virtual environment."
        python -m venv .venv
        Assert-LastExitCode "python -m venv .venv"
        & $venvPython -m pip install --upgrade pip
        Assert-LastExitCode "pip install --upgrade pip"
        & $venvPython -m pip install -e ".[dev]"
        Assert-LastExitCode "pip install -e .[dev]"
    }

    $python = Get-PythonForRepo -RepoRoot $RepoDir
    Write-Step "Starting support worker with Python: $python"

    $workerArgs = @(
        "-WorkerName", $WorkerName,
        "-CycleMinutes", "0",
        "-FullSeedSweepEvery", "3",
        "-Python", $python
    )
    if ($KeepDisplayOff) {
        $workerArgs += "-KeepDisplayOff"
    }
    if ($Detached) {
        $workerArgs += "-Detached"
    }

    & ".\scripts\run_problem_3_support_worker.ps1" @workerArgs
}
finally {
    Pop-Location
}
