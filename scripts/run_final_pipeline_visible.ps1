param(
    [int[]]$Seeds = (1..20),
    [string]$SeedSweepOutputRoot = "results/problem_3_seed_sweep",
    [string]$Python = ""
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectPython {
    param([string]$RequestedPython)

    if ($RequestedPython) {
        if (Test-Path -LiteralPath $RequestedPython) {
            return (Resolve-Path -LiteralPath $RequestedPython).Path
        }
        throw "Python path does not exist: $RequestedPython"
    }

    $venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPython) {
        return $venvPython
    }

    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    throw "Could not find python. Pass -Python or activate a Python environment."
}

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$projectPython = Resolve-ProjectPython -RequestedPython $Python

Push-Location $repoRoot
try {
    Write-Step "Final automated pipeline started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Python: $projectPython"

    Write-Step "Initial git status."
    git status --short --branch

    Write-Step "Running tests."
    & $projectPython -m pytest --basetemp .pytest_tmp_final
    if ($LASTEXITCODE -ne 0) {
        throw "pytest failed with exit code $LASTEXITCODE"
    }

    Write-Step "Running simple submission layer."
    & $projectPython submission/run_all.py
    if ($LASTEXITCODE -ne 0) {
        throw "submission/run_all.py failed with exit code $LASTEXITCODE"
    }

    Write-Step "Running visible Problem 3 seed sweep."
    & (Join-Path $PSScriptRoot "run_problem_3_seed_sweep_visible.ps1") `
        -Seeds $Seeds `
        -OutputRoot $SeedSweepOutputRoot `
        -Python $projectPython `
        -SkipTests
    if ($LASTEXITCODE -ne 0) {
        throw "Problem 3 seed sweep failed with exit code $LASTEXITCODE"
    }

    Write-Step "Final git status."
    git status --short --branch

    $submissionSummary = Join-Path $repoRoot "results/submission_simple/SUMMARY.md"
    $seedSummary = Join-Path $repoRoot "$SeedSweepOutputRoot/seed_sweep_summary.md"

    Write-Step "Final summaries."
    if (Test-Path -LiteralPath $submissionSummary) {
        Write-Host ""
        Get-Content -LiteralPath $submissionSummary -Encoding UTF8
    }
    if (Test-Path -LiteralPath $seedSummary) {
        Write-Host ""
        Get-Content -LiteralPath $seedSummary -Encoding UTF8
    }

    Write-Step "Final automated pipeline finished."
}
finally {
    Pop-Location
}
