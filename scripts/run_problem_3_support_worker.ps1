param(
    [string]$WorkerName = "support",
    [int]$CycleMinutes = 0,
    [int]$MaxCycles = 0,
    [int]$FullSeedSweepEvery = 3,
    [int[]]$HybridSeeds = (2026, 2027),
    [double[]]$AngleScales = (0.5, 3.141592653589793),
    [int[]]$SweepSeeds = (1..20),
    [string]$StatusOutput = "",
    [string]$ProgressLog = "",
    [string]$LogRoot = "",
    [string]$Python = "",
    [switch]$KeepDisplayOff,
    [switch]$SkipTeamSync,
    [switch]$SkipTests,
    [switch]$SkipSubmissionQuick,
    [switch]$SkipSeedSweep,
    [switch]$Detached,
    [switch]$StatusOnly
)

$ErrorActionPreference = "Stop"

function ConvertTo-CommandLineArgument {
    param([string]$Argument)

    if ($Argument -notmatch '[\s"]') {
        return $Argument
    }

    return '"' + ($Argument -replace '"', '\"') + '"'
}

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Get-SafeName {
    param([string]$Name)
    $safe = $Name -replace '[^A-Za-z0-9_.-]', '_'
    if (-not $safe) {
        return "support"
    }
    return $safe
}

function Resolve-RepoPath {
    param([string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return (Join-Path $repoRoot $Path)
}

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

function Assert-LastExitCode {
    param([string]$CommandName)

    if ($LASTEXITCODE -ne 0) {
        throw "$CommandName failed with exit code $LASTEXITCODE"
    }
}

function Initialize-KeepAwake {
    param([switch]$DisplayOff)

    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Support.PowerManagement").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderP3Support {
    public static class PowerManagement {
        [DllImport("kernel32.dll")]
        public static extern uint SetThreadExecutionState(uint esFlags);
    }
}
"@
    }

    [uint32]$ES_CONTINUOUS = 2147483648
    [uint32]$ES_SYSTEM_REQUIRED = 1
    [uint32]$ES_DISPLAY_REQUIRED = 2

    $flags = $ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED
    if (-not $DisplayOff) {
        $flags = $flags -bor $ES_DISPLAY_REQUIRED
    }

    [QuantumCylinderP3Support.PowerManagement]::SetThreadExecutionState([uint32]$flags) | Out-Null
}

function Clear-KeepAwake {
    if (([System.Management.Automation.PSTypeName]"QuantumCylinderP3Support.PowerManagement").Type) {
        [QuantumCylinderP3Support.PowerManagement]::SetThreadExecutionState([uint32]2147483648) | Out-Null
    }
}

function Disable-QuickEditMode {
    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Support.ConsoleMode").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderP3Support {
    public static class ConsoleMode {
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern IntPtr GetStdHandle(int nStdHandle);

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool GetConsoleMode(IntPtr hConsoleHandle, out int lpMode);

        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern bool SetConsoleMode(IntPtr hConsoleHandle, int dwMode);
    }
}
"@
    }

    $STD_INPUT_HANDLE = -10
    $ENABLE_QUICK_EDIT_MODE = 0x0040
    $ENABLE_EXTENDED_FLAGS = 0x0080

    $handle = [QuantumCylinderP3Support.ConsoleMode]::GetStdHandle($STD_INPUT_HANDLE)
    if ($handle -eq [IntPtr]::Zero -or $handle.ToInt64() -eq -1) {
        return $null
    }

    $mode = 0
    if (-not [QuantumCylinderP3Support.ConsoleMode]::GetConsoleMode($handle, [ref]$mode)) {
        return $null
    }

    $newMode = ($mode -bor $ENABLE_EXTENDED_FLAGS) -band (-bnot $ENABLE_QUICK_EDIT_MODE)
    [QuantumCylinderP3Support.ConsoleMode]::SetConsoleMode($handle, $newMode) | Out-Null

    return @{
        Handle = $handle
        Mode = $mode
    }
}

function Restore-ConsoleMode {
    param($ConsoleState)

    if ($ConsoleState -and ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Support.ConsoleMode").Type) {
        [QuantumCylinderP3Support.ConsoleMode]::SetConsoleMode($ConsoleState.Handle, $ConsoleState.Mode) | Out-Null
    }
}

function Format-RunDuration {
    param([TimeSpan]$Duration)
    return ("{0:00}:{1:00}:{2:00}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds)
}

function Format-AngleLabel {
    param([double]$Angle)

    if ([math]::Abs($Angle - [math]::PI) -lt 0.000001) {
        return "pi"
    }
    return ("{0:0.000000}" -f $Angle).Replace("-", "m").Replace(".", "p")
}

function Initialize-ProgressLog {
    param([string]$Path)

    $resolved = Resolve-RepoPath -Path $Path
    $parent = Split-Path -Parent $resolved
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    if (-not (Test-Path -LiteralPath $resolved)) {
        @(
            "# Problem 3 Support Worker Progress Log",
            "",
            "This log is generated locally and is not committed by default.",
            "",
            "- worker: ``$WorkerName``",
            "- purpose: independent evidence generation without source edits",
            ""
        ) | Set-Content -LiteralPath $resolved -Encoding UTF8
    }
}

function Add-ProgressLogEntry {
    param(
        [string]$Path,
        [object]$CycleResult
    )

    $resolved = Resolve-RepoPath -Path $Path
    $lines = @(
        "",
        "## Cycle $($CycleResult.cycle) - $($CycleResult.status)",
        "",
        "- started_at: ``$($CycleResult.started_at)``",
        "- finished_at: ``$($CycleResult.finished_at)``",
        "- duration: ``$($CycleResult.duration)``",
        "- hybrid runs: ``$($CycleResult.hybrid_runs)``",
        "- seed sweep: ``$($CycleResult.seed_sweep)``",
        "- note: $($CycleResult.note)"
    )
    Add-Content -LiteralPath $resolved -Value $lines -Encoding UTF8
}

function Get-GitStatusText {
    $lines = @(git status --short --branch)
    if ($lines.Count -eq 0) {
        return "clean"
    }
    return ($lines -join "`n")
}

function Invoke-TeamSyncIfClean {
    if ($SkipTeamSync) {
        Write-Step "SKIP: team sync"
        return "skipped"
    }

    Write-Step "START: safe fetch/pull"
    git fetch --prune origin
    Assert-LastExitCode "git fetch --prune origin"

    $branch = (git branch --show-current).Trim()
    if ($branch -ne "main") {
        Write-Step "Current branch is '$branch', not main. Fetch completed; pull skipped."
        return "fetch-only-non-main"
    }

    $trackedChanges = @(git status --porcelain --untracked-files=no | Where-Object { $_ })
    if ($trackedChanges.Count -gt 0) {
        Write-Step "Tracked local changes exist. Pull skipped to avoid conflicts."
        $trackedChanges | ForEach-Object { Write-Host "  $_" }
        return "fetch-only-local-changes"
    }

    git pull --ff-only origin main
    Assert-LastExitCode "git pull --ff-only origin main"
    Write-Step "PASS: safe fetch/pull"
    return "pulled"
}

function Invoke-Verification {
    param([string]$Phase)

    if (-not $SkipTests) {
        Write-Step "START: pytest ($Phase)"
        & $projectPython -m pytest --basetemp ".pytest_tmp_p3_support_$Phase"
        Assert-LastExitCode "pytest ($Phase)"
        Write-Step "PASS: pytest ($Phase)"
    }
    else {
        Write-Step "SKIP: pytest ($Phase)"
    }

    if (-not $SkipSubmissionQuick) {
        Write-Step "START: submission quick ($Phase)"
        & $projectPython submission/run_all.py --quick
        Assert-LastExitCode "submission/run_all.py --quick ($Phase)"
        Write-Step "PASS: submission quick ($Phase)"
    }
    else {
        Write-Step "SKIP: submission quick ($Phase)"
    }
}

function Invoke-HybridGrid {
    param([int]$Cycle)

    $runCount = 0
    $cycleOutputRoot = Resolve-RepoPath -Path (Join-Path $workerResultRoot "cycle_$Cycle")
    New-Item -ItemType Directory -Force -Path $cycleOutputRoot | Out-Null

    foreach ($seed in $HybridSeeds) {
        foreach ($angle in $AngleScales) {
            $angleLabel = Format-AngleLabel -Angle $angle
            $outputDir = Join-Path $cycleOutputRoot "hybrid_seed_${seed}_angle_$angleLabel"
            $logPath = Join-Path $logRootPath "cycle_${Cycle}_hybrid_seed_${seed}_angle_$angleLabel.log"
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $logPath) | Out-Null

            Write-Step "START: hybrid toy seed=$seed angle=$angle output=$outputDir"
            & $projectPython scripts/run_problem_3_hybrid_diffusion_toy.py `
                --seed $seed `
                --angle-scale $angle `
                --output-dir $outputDir 2>&1 | Tee-Object -FilePath $logPath | ForEach-Object { Write-Host $_ }
            Assert-LastExitCode "hybrid toy seed=$seed angle=$angle"
            Write-Step "PASS: hybrid toy seed=$seed angle=$angle"
            $runCount += 1
        }
    }

    return $runCount
}

function Invoke-SeedSweepIfNeeded {
    param([int]$Cycle)

    if ($SkipSeedSweep) {
        Write-Step "SKIP: seed sweep"
        return "skipped"
    }
    if ($FullSeedSweepEvery -le 0) {
        Write-Step "SKIP: seed sweep disabled"
        return "disabled"
    }
    if (($Cycle % $FullSeedSweepEvery) -ne 0) {
        Write-Step "SKIP: seed sweep; cycle $Cycle is not a multiple of $FullSeedSweepEvery"
        return "not-due"
    }

    $seedSweepScript = Join-Path $PSScriptRoot "run_problem_3_seed_sweep_visible.ps1"
    $relativeOutput = Join-Path $workerResultRoot "seed_sweep_cycle_$Cycle"
    $logPath = Join-Path $logRootPath "cycle_${Cycle}_seed_sweep.log"

    Write-Step "START: support seed sweep cycle=$Cycle output=$relativeOutput"
    & $seedSweepScript `
        -Seeds $SweepSeeds `
        -OutputRoot $relativeOutput `
        -Python $projectPython `
        -SkipTests 2>&1 | Tee-Object -FilePath $logPath | ForEach-Object { Write-Host $_ }
    Assert-LastExitCode "support seed sweep cycle=$Cycle"
    Write-Step "PASS: support seed sweep cycle=$Cycle"
    return "passed"
}

function Write-WorkerStatus {
    param(
        [string]$Path,
        [string]$Mode
    )

    $resolved = Resolve-RepoPath -Path $Path
    $parent = Split-Path -Parent $resolved
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $statusLines = @(
        "# Problem 3 Support Worker Status",
        "",
        "- generated_at: ``$(Get-Date -Format s)``",
        "- mode: ``$Mode``",
        "- worker: ``$WorkerName``",
        "- branch: ``$((git branch --show-current).Trim())``",
        "- cycle_minutes: ``$CycleMinutes``",
        "- max_cycles: ``$MaxCycles`` (``0`` means run until Ctrl+C)",
        "- full_seed_sweep_every: ``$FullSeedSweepEvery``",
        "- hybrid_seeds: ``$($HybridSeeds -join ', ')``",
        "- angle_scales: ``$($AngleScales -join ', ')``",
        "- result_root: ``$workerResultRoot``",
        "- progress_log: ``$ProgressLog``",
        "- logs: ``$LogRoot``",
        "",
        "## Role",
        "",
        "This worker is evidence-only. It should not edit source files, sync GitHub issues, create PRs, or merge branches. The main Jihoo automation remains the strategy/code owner; this worker produces independent reproducibility and ablation evidence.",
        "",
        "## Recent Cycles",
        ""
    )

    if ($script:CycleResults.Count -eq 0) {
        $statusLines += "- no cycle has run yet"
    }
    else {
        foreach ($result in ($script:CycleResults | Select-Object -Last 8)) {
            $statusLines += "- cycle $($result.cycle): $($result.status), duration $($result.duration), hybrid runs $($result.hybrid_runs), seed sweep $($result.seed_sweep)"
        }
    }

    $statusLines += @(
        "",
        "## Safe Claim Guardrail",
        "",
        "Use support-worker results as robustness or ablation evidence only. Do not claim hardware advantage, general quantum advantage, or a full trainable QuDDPM reverse process from this script.",
        "",
        "## Git Status",
        "",
        '```text',
        (Get-GitStatusText),
        '```'
    )

    $statusLines | Set-Content -LiteralPath $resolved -Encoding UTF8
}

function Start-DetachedWorker {
    $outerOutLog = Join-Path $logRootPath "detached_stdout.log"
    $outerErrLog = Join-Path $logRootPath "detached_stderr.log"
    $pidPath = Join-Path $logRootPath "detached_process.json"
    New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null

    $childArgs = @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $PSCommandPath,
        "-WorkerName", $WorkerName,
        "-CycleMinutes", [string]$CycleMinutes,
        "-MaxCycles", [string]$MaxCycles,
        "-FullSeedSweepEvery", [string]$FullSeedSweepEvery,
        "-HybridSeeds", ($HybridSeeds -join ","),
        "-AngleScales", ($AngleScales -join ","),
        "-SweepSeeds", ($SweepSeeds -join ","),
        "-StatusOutput", $StatusOutput,
        "-ProgressLog", $ProgressLog,
        "-LogRoot", $LogRoot
    )

    if ($Python) {
        $childArgs += @("-Python", $Python)
    }
    if ($KeepDisplayOff) {
        $childArgs += "-KeepDisplayOff"
    }
    if ($SkipTeamSync) {
        $childArgs += "-SkipTeamSync"
    }
    if ($SkipTests) {
        $childArgs += "-SkipTests"
    }
    if ($SkipSubmissionQuick) {
        $childArgs += "-SkipSubmissionQuick"
    }
    if ($SkipSeedSweep) {
        $childArgs += "-SkipSeedSweep"
    }

    $commandLine = ($childArgs | ForEach-Object { ConvertTo-CommandLineArgument $_ }) -join " "
    $process = Start-Process `
        -FilePath (Get-Command powershell.exe).Source `
        -ArgumentList $commandLine `
        -WorkingDirectory $repoRoot `
        -RedirectStandardOutput $outerOutLog `
        -RedirectStandardError $outerErrLog `
        -WindowStyle Hidden `
        -PassThru

    @{
        pid = $process.Id
        started_at = (Get-Date).ToString("s")
        stdout_log = $outerOutLog
        stderr_log = $outerErrLog
        status = "started"
        command = "powershell.exe $commandLine"
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $pidPath -Encoding UTF8

    Write-Step "Detached Problem 3 support worker started with PID $($process.Id)."
    Write-Step "Status: $(Resolve-RepoPath -Path $StatusOutput)"
    Write-Step "Stop with: .\scripts\stop_problem_3_support_worker.ps1 -WorkerName $WorkerName"
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$safeWorkerName = Get-SafeName -Name $WorkerName

if (-not $StatusOutput) {
    $StatusOutput = "results/problem_3_support_worker/$safeWorkerName/latest_status.md"
}
if (-not $ProgressLog) {
    $ProgressLog = "results/problem_3_support_worker/$safeWorkerName/progress_log.md"
}
if (-not $LogRoot) {
    $LogRoot = "logs/problem_3_support_worker/$safeWorkerName"
}

$workerResultRoot = "results/problem_3_support_worker/$safeWorkerName"
$logRootPath = Resolve-RepoPath -Path $LogRoot
$projectPython = Resolve-ProjectPython -RequestedPython $Python
$script:CycleResults = @()
$consoleState = $null

Push-Location $repoRoot
try {
    if ($Detached) {
        Start-DetachedWorker
        return
    }

    $consoleState = Disable-QuickEditMode
    Initialize-KeepAwake -DisplayOff:$KeepDisplayOff
    New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null
    Initialize-ProgressLog -Path $ProgressLog

    Write-Step "Problem 3 support worker started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Worker: $WorkerName"
    Write-Step "Python: $projectPython"
    Write-Step "Hybrid seeds: $($HybridSeeds -join ', ')"
    Write-Step "Angle scales: $($AngleScales -join ', ')"
    Write-Step "Full seed sweep every: $FullSeedSweepEvery"

    if ($CycleMinutes -lt 0) {
        throw "CycleMinutes must be 0 or greater."
    }
    if ($FullSeedSweepEvery -lt 0) {
        throw "FullSeedSweepEvery must be 0 or greater."
    }

    if ($StatusOnly) {
        Write-WorkerStatus -Path $StatusOutput -Mode "status-only"
        Write-Step "Status-only mode finished."
        return
    }

    $cycle = 0
    while ($true) {
        $cycle += 1
        $startedAt = Get-Date
        $status = "pass"
        $note = "Support worker cycle completed."
        $hybridRuns = 0
        $seedSweepStatus = "not-started"

        Write-Step "START: Problem 3 support worker cycle $cycle"
        try {
            Invoke-TeamSyncIfClean | Out-Null
            Invoke-Verification -Phase "before_cycle_$cycle"
            $hybridRuns = Invoke-HybridGrid -Cycle $cycle
            $seedSweepStatus = Invoke-SeedSweepIfNeeded -Cycle $cycle
            Invoke-Verification -Phase "after_cycle_$cycle"
        }
        catch {
            $status = "failed"
            $note = $_.Exception.Message
            Write-Step "FAILED: Problem 3 support worker cycle $cycle"
            Write-Host $note -ForegroundColor Yellow
        }

        $endedAt = Get-Date
        $duration = New-TimeSpan -Start $startedAt -End $endedAt
        $cycleResult = [pscustomobject]@{
            cycle = $cycle
            status = $status
            started_at = $startedAt.ToString("s")
            finished_at = $endedAt.ToString("s")
            duration = (Format-RunDuration -Duration $duration)
            note = $note
            hybrid_runs = $hybridRuns
            seed_sweep = $seedSweepStatus
        }
        $script:CycleResults += $cycleResult

        Add-ProgressLogEntry -Path $ProgressLog -CycleResult $cycleResult
        Write-WorkerStatus -Path $StatusOutput -Mode "continuous"
        Write-Step "END: Problem 3 support worker cycle $cycle with status $status"

        if ($MaxCycles -gt 0 -and $cycle -ge $MaxCycles) {
            Write-Step "Reached MaxCycles=$MaxCycles. Support worker finished."
            break
        }

        if ($CycleMinutes -eq 0) {
            Write-Step "Starting next support cycle immediately. Press Ctrl+C to stop."
            continue
        }

        $sleepSeconds = $CycleMinutes * 60
        Write-Step "Sleeping for $CycleMinutes minutes before next support cycle. Press Ctrl+C to stop."
        Start-Sleep -Seconds $sleepSeconds
    }
}
finally {
    Clear-KeepAwake
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
}
