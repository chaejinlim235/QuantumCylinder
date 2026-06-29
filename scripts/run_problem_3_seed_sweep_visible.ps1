param(
    [int[]]$Seeds = (1..20),
    [string]$OutputRoot = "results/problem_3_seed_sweep",
    [string]$Python = "",
    [switch]$SkipTests
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

function Format-Duration {
    param([TimeSpan]$Duration)
    if ($Duration.TotalHours -ge 1) {
        return "{0:D2}:{1:D2}:{2:D2}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds
    }
    return "{0:D2}:{1:D2}" -f [int]$Duration.TotalMinutes, $Duration.Seconds
}

function Resolve-SeedLogPath {
    param(
        [string]$LogRoot,
        [int]$Seed
    )

    $baseLog = Join-Path $LogRoot "seed_$Seed.log"
    try {
        $stream = [System.IO.File]::Open(
            $baseLog,
            [System.IO.FileMode]::Create,
            [System.IO.FileAccess]::Write,
            [System.IO.FileShare]::Read
        )
        $stream.Close()
        return $baseLog
    }
    catch {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $alternateLog = Join-Path $LogRoot "seed_${Seed}_$stamp.log"
        Write-Step "Seed $Seed log is locked; using alternate log: $alternateLog"
        return $alternateLog
    }
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$projectPython = Resolve-ProjectPython -RequestedPython $Python
$outputRootPath = Join-Path $repoRoot $OutputRoot
$logRoot = Join-Path $outputRootPath "logs"

Push-Location $repoRoot
try {
    New-Item -ItemType Directory -Force -Path $outputRootPath | Out-Null
    New-Item -ItemType Directory -Force -Path $logRoot | Out-Null

    Write-Step "Problem 3 visible seed sweep started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Python: $projectPython"
    Write-Step "Output: $outputRootPath"
    Write-Step "Seeds: $($Seeds -join ', ')"

    if (-not $SkipTests) {
        Write-Step "Running tests: python -m pytest"
        & $projectPython -m pytest --basetemp .pytest_tmp_visible
        if ($LASTEXITCODE -ne 0) {
            throw "pytest failed with exit code $LASTEXITCODE"
        }
        Write-Step "Tests passed."
    }

    $totalWatch = [System.Diagnostics.Stopwatch]::StartNew()
    $completed = 0

    foreach ($seed in $Seeds) {
        $completed += 1
        $seedDir = Join-Path $outputRootPath "seed_$seed"
        $seedLog = Resolve-SeedLogPath -LogRoot $logRoot -Seed $seed
        $seedWatch = [System.Diagnostics.Stopwatch]::StartNew()

        Write-Progress `
            -Activity "Problem 3 seed sweep" `
            -Status "Running seed $seed ($completed / $($Seeds.Count))" `
            -PercentComplete (($completed - 1) * 100 / $Seeds.Count)

        Write-Step "Seed $seed started. Output: $seedDir"
        & $projectPython scripts/run_problem_3_continuous_denoising.py `
            --seed $seed `
            --output-dir $seedDir 2>&1 | Tee-Object -FilePath $seedLog
        if ($LASTEXITCODE -ne 0) {
            throw "Seed $seed failed with exit code $LASTEXITCODE. See $seedLog"
        }

        $seedWatch.Stop()
        $summaryPath = Join-Path $seedDir "problem_3_summary.md"
        if (Test-Path -LiteralPath $summaryPath) {
            $decisionLine = Select-String -Path $summaryPath -Pattern "Overall decision:" | Select-Object -First 1
            if ($decisionLine) {
                Write-Step "Seed $seed decision: $($decisionLine.Line.Trim())"
            }
        }
        Write-Step "Seed $seed finished in $(Format-Duration $seedWatch.Elapsed). Log: $seedLog"
    }

    Write-Progress -Activity "Problem 3 seed sweep" -Completed
    Write-Step "Aggregating seed results."
    & $projectPython scripts/summarize_problem_3_seed_sweep.py --input-dir $OutputRoot --seeds $Seeds
    if ($LASTEXITCODE -ne 0) {
        throw "Seed sweep aggregation failed with exit code $LASTEXITCODE"
    }

    $summary = Join-Path $outputRootPath "seed_sweep_summary.md"
    $totalWatch.Stop()
    Write-Step "Visible seed sweep finished in $(Format-Duration $totalWatch.Elapsed)."
    Write-Step "Summary: $summary"
    Write-Host ""
    Get-Content -LiteralPath $summary -Encoding UTF8
}
finally {
    Pop-Location
}
