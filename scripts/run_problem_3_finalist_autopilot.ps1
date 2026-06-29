param(
    [int]$CycleMinutes = 0,
    [int]$MaxCycles = 0,
    [int]$HermesMaxTurns = 620,
    [int]$HermesAttempts = 3,
    [int]$HermesRetryDelaySeconds = 30,
    [int]$HermesHeartbeatSeconds = 30,
    [int]$IdleTimeoutMinutes = 60,
    [int]$FullSeedSweepEvery = 3,
    [double]$RunHours = 0,
    [string]$StopAt = "",
    [int]$MinRemainingMinutesForNextCycle = 0,
    [int[]]$Seeds = (1..20),
    [string]$SeedList = "",
    [string]$StatusOutput = "results/problem_3_finalist_autopilot/latest_status.md",
    [string]$ProgressLog = "results/problem_3_finalist_autopilot/progress_log.md",
    [string]$LogRoot = "logs/problem_3_finalist_autopilot",
    [string]$Python = "",
    [switch]$KeepDisplayOff,
    [switch]$AllowNonMainBranch,
    [switch]$SkipTeamSync,
    [switch]$SkipTests,
    [switch]$SkipSubmissionQuick,
    [switch]$SkipIssueSync,
    [switch]$Detached,
    [switch]$StatusOnly
)

$ErrorActionPreference = "Stop"

if ($SeedList) {
    $parsedSeeds = @()
    foreach ($rawSeed in ($SeedList -split ",")) {
        $trimmedSeed = $rawSeed.Trim()
        if (-not $trimmedSeed) {
            continue
        }
        $parsedSeeds += [int]::Parse($trimmedSeed, [System.Globalization.CultureInfo]::InvariantCulture)
    }
    if ($parsedSeeds.Count -eq 0) {
        throw "SeedList was provided but no valid seeds were parsed."
    }
    $Seeds = [int[]]$parsedSeeds
}

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

    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Finalist.PowerManagement").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderP3Finalist {
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

    [QuantumCylinderP3Finalist.PowerManagement]::SetThreadExecutionState([uint32]$flags) | Out-Null
}

function Clear-KeepAwake {
    if (([System.Management.Automation.PSTypeName]"QuantumCylinderP3Finalist.PowerManagement").Type) {
        [QuantumCylinderP3Finalist.PowerManagement]::SetThreadExecutionState([uint32]2147483648) | Out-Null
    }
}

function Disable-QuickEditMode {
    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Finalist.ConsoleMode").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderP3Finalist {
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

    $handle = [QuantumCylinderP3Finalist.ConsoleMode]::GetStdHandle($STD_INPUT_HANDLE)
    if ($handle -eq [IntPtr]::Zero -or $handle.ToInt64() -eq -1) {
        return $null
    }

    $mode = 0
    if (-not [QuantumCylinderP3Finalist.ConsoleMode]::GetConsoleMode($handle, [ref]$mode)) {
        return $null
    }

    $newMode = ($mode -bor $ENABLE_EXTENDED_FLAGS) -band (-bnot $ENABLE_QUICK_EDIT_MODE)
    [QuantumCylinderP3Finalist.ConsoleMode]::SetConsoleMode($handle, $newMode) | Out-Null

    return @{
        Handle = $handle
        Mode = $mode
    }
}

function Restore-ConsoleMode {
    param($ConsoleState)

    if ($ConsoleState -and ([System.Management.Automation.PSTypeName]"QuantumCylinderP3Finalist.ConsoleMode").Type) {
        [QuantumCylinderP3Finalist.ConsoleMode]::SetConsoleMode($ConsoleState.Handle, $ConsoleState.Mode) | Out-Null
    }
}

function Format-RunDuration {
    param([TimeSpan]$Duration)
    return ("{0:00}:{1:00}:{2:00}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds)
}

function Resolve-Deadline {
    $deadlines = @()
    if ($RunHours -gt 0) {
        $deadlines += (Get-Date).AddHours($RunHours)
    }
    if ($StopAt) {
        try {
            $deadlines += [datetime]::Parse($StopAt)
        }
        catch {
            throw "StopAt must be parseable as a datetime, for example 2026-06-30T08:00:00. Got: $StopAt"
        }
    }
    if ($deadlines.Count -eq 0) {
        return $null
    }
    return ($deadlines | Sort-Object | Select-Object -First 1)
}

function Format-Deadline {
    param($Deadline)

    if ($null -eq $Deadline) {
        return "none"
    }
    return $Deadline.ToString("s")
}

function Get-RemainingUntilDeadline {
    param($Deadline)

    if ($null -eq $Deadline) {
        return $null
    }
    return New-TimeSpan -Start (Get-Date) -End $Deadline
}

function Test-ShouldStartCycle {
    param($Deadline)

    if ($null -eq $Deadline) {
        return $true
    }

    $remaining = Get-RemainingUntilDeadline -Deadline $Deadline
    if ($remaining.TotalSeconds -le 0) {
        Write-Step "Stop deadline already reached: $(Format-Deadline -Deadline $Deadline)"
        return $false
    }
    if ($remaining.TotalMinutes -lt $MinRemainingMinutesForNextCycle) {
        Write-Step "Only $([math]::Round($remaining.TotalMinutes, 1)) minutes remain before deadline; not starting another cycle."
        return $false
    }
    return $true
}

function Resolve-RepoPath {
    param([string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return Join-Path $repoRoot $Path
}

function Set-SharedUtf8Text {
    param(
        [string]$Path,
        [string]$Text
    )

    $encoding = [System.Text.UTF8Encoding]::new($false)
    for ($attempt = 1; $attempt -le 20; $attempt++) {
        try {
            $stream = [System.IO.File]::Open(
                $Path,
                [System.IO.FileMode]::Create,
                [System.IO.FileAccess]::Write,
                [System.IO.FileShare]::ReadWrite
            )
            try {
                $writer = [System.IO.StreamWriter]::new($stream, $encoding)
                $stream = $null
                try {
                    $writer.Write($Text)
                }
                finally {
                    $writer.Dispose()
                }
            }
            finally {
                if ($stream) {
                    $stream.Dispose()
                }
            }
            return
        }
        catch {
            if ($attempt -eq 20) {
                throw
            }
            Start-Sleep -Milliseconds 250
        }
    }
}

function Add-SharedUtf8Text {
    param(
        [string]$Path,
        [string]$Text
    )

    $encoding = [System.Text.UTF8Encoding]::new($false)
    for ($attempt = 1; $attempt -le 20; $attempt++) {
        try {
            $stream = [System.IO.File]::Open(
                $Path,
                [System.IO.FileMode]::Append,
                [System.IO.FileAccess]::Write,
                [System.IO.FileShare]::ReadWrite
            )
            try {
                $writer = [System.IO.StreamWriter]::new($stream, $encoding)
                $stream = $null
                try {
                    $writer.Write($Text)
                }
                finally {
                    $writer.Dispose()
                }
            }
            finally {
                if ($stream) {
                    $stream.Dispose()
                }
            }
            return
        }
        catch {
            if ($attempt -eq 20) {
                throw
            }
            Start-Sleep -Milliseconds 250
        }
    }
}

function Get-FileTextIfExists {
    param([string]$Path)

    if (Test-Path -LiteralPath $Path) {
        return Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    }
    return ""
}

function Get-MarkdownMetric {
    param(
        [string]$Text,
        [string]$Label
    )

    $escaped = [regex]::Escape($Label)
    $pattern = '(?m)^\s*(?:-\s*)?' + $escaped + '\s*:\s*`([^`]+)`'
    $match = [regex]::Match($Text, $pattern)
    if ($match.Success) {
        return $match.Groups[1].Value
    }
    return ""
}

function Get-Problem3Metrics {
    $seedSummaryPath = Join-Path $repoRoot "results\problem_3_seed_sweep\seed_sweep_summary.md"
    $seedSummary = Get-FileTextIfExists -Path $seedSummaryPath

    return @{
        recommendation = Get-MarkdownMetric -Text $seedSummary -Label "Main-claim recommendation"
        total_seeds = Get-MarkdownMetric -Text $seedSummary -Label "Total seeds"
        use_as_main = Get-MarkdownMetric -Text $seedSummary -Label "use_as_main"
        main_fraction = Get-MarkdownMetric -Text $seedSummary -Label "main_candidate row fraction"
        mmd_improvement = Get-MarkdownMetric -Text $seedSummary -Label "continuous_mmd_improvement"
        wasserstein_improvement = Get-MarkdownMetric -Text $seedSummary -Label "continuous_wasserstein_improvement"
        axis_margin = Get-MarkdownMetric -Text $seedSummary -Label "continuous_score_minus_axis_score"
        diversity = Get-MarkdownMetric -Text $seedSummary -Label "continuous_diversity_retention"
        success_probability = Get-MarkdownMetric -Text $seedSummary -Label "continuous_mean_success_probability"
        nonpositive_axis_rows = Get-MarkdownMetric -Text $seedSummary -Label "nonpositive axis-margin rows"
    }
}

function Get-HybridToyMetrics {
    $hybridSummaryPath = Join-Path $repoRoot "results\problem_3_hybrid_diffusion_toy\hybrid_toy_summary.md"
    $hybridSummary = Get-FileTextIfExists -Path $hybridSummaryPath

    return @{
        positive_rows = Get-MarkdownMetric -Text $hybridSummary -Label "positive-improvement rows"
        mmd_improvement = Get-MarkdownMetric -Text $hybridSummary -Label "median MMD improvement"
        wasserstein_improvement = Get-MarkdownMetric -Text $hybridSummary -Label "median Wasserstein improvement"
        diversity = Get-MarkdownMetric -Text $hybridSummary -Label "median diversity retention"
        success_probability = Get-MarkdownMetric -Text $hybridSummary -Label "median success probability"
    }
}

function Get-CurrentChangeLines {
    $tracked = @(git diff --name-status)
    $staged = @(git diff --cached --name-status)
    $untracked = @(git ls-files --others --exclude-standard | Where-Object {
        $_ -notmatch '^(results|logs)/' -and $_ -notmatch '^(results|logs)\\'
    } | ForEach-Object { "?? $($_)" })

    $changes = @()
    $changes += $tracked
    $changes += $staged
    $changes += $untracked

    if ($changes.Count -eq 0) {
        return @("none")
    }

    return @($changes | Select-Object -Unique)
}

function Initialize-ProgressLog {
    param([string]$Path)

    $resolvedPath = Resolve-RepoPath -Path $Path
    $logDir = Split-Path -Parent $resolvedPath
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null

    if (-not (Test-Path -LiteralPath $resolvedPath)) {
        $lines = @(
            "# Problem 3 Finalist Autopilot Progress Log",
            "",
            "This generated log records each autopilot cycle.",
            "",
            '- source status: generated under `results/`, ignored by Git',
            '- main status file: `results/problem_3_finalist_autopilot/latest_status.md`',
            '- detailed logs: `logs/problem_3_finalist_autopilot/`',
            ""
        )
        Set-SharedUtf8Text -Path $resolvedPath -Text (($lines -join "`n") + "`n")
    }

    return $resolvedPath
}

function Add-ProgressLogEntry {
    param(
        [string]$Path,
        [pscustomobject]$CycleResult,
        [string[]]$ChangeLines
    )

    $resolvedPath = Initialize-ProgressLog -Path $Path
    $metrics = Get-Problem3Metrics
    $gitHead = (git rev-parse --short HEAD).Trim()
    $branch = (git branch --show-current).Trim()
    $changeMarkdown = @($ChangeLines | ForEach-Object { "- $_" })

    $entry = @(
        "## Cycle $($CycleResult.cycle) - $($CycleResult.finished_at)",
        "",
        ('- status: `{0}`' -f $CycleResult.status),
        ('- branch: `{0}`' -f $branch),
        ('- head: `{0}`' -f $gitHead),
        ('- started_at: `{0}`' -f $CycleResult.started_at),
        ('- finished_at: `{0}`' -f $CycleResult.finished_at),
        ('- duration: `{0}`' -f $CycleResult.duration),
        ('- seed_sweep: `{0}`' -f $CycleResult.seed_sweep),
        ('- note: {0}' -f $CycleResult.note),
        ('- recommendation: `{0}`' -f $metrics.recommendation),
        ('- MMD improvement: `{0}`' -f $metrics.mmd_improvement),
        ('- Wasserstein improvement: `{0}`' -f $metrics.wasserstein_improvement),
        ('- axis-only score margin: `{0}`' -f $metrics.axis_margin),
        ('- diversity retention: `{0}`' -f $metrics.diversity),
        ('- success probability: `{0}`' -f $metrics.success_probability),
        "",
        "### Current Source Changes",
        ""
    ) + $changeMarkdown + @("")

    Add-SharedUtf8Text -Path $resolvedPath -Text (($entry -join "`n") + "`n")
    Write-Step "Appended progress log: $resolvedPath"
}

function Write-AutopilotStatus {
    param(
        [string]$Path,
        [string]$Mode
    )

    $resolvedPath = Resolve-RepoPath -Path $Path
    $statusDir = Split-Path -Parent $resolvedPath
    New-Item -ItemType Directory -Force -Path $statusDir | Out-Null

    $metrics = Get-Problem3Metrics
    $hybridMetrics = Get-HybridToyMetrics
    $branch = (git branch --show-current).Trim()
    $gitStatus = @(git status --short --branch)
    $cycleLines = if ($script:CycleResults.Count -gt 0) {
        @($script:CycleResults | Select-Object -Last 12 | ForEach-Object {
            "- cycle {0}: `{1}` started `{2}`, duration `{3}`, seed_sweep `{4}`, changes `{5}` - {6}" -f `
                $_.cycle, `
                $_.status, `
                $_.started_at, `
                $_.duration, `
                $_.seed_sweep, `
                $_.changed_files, `
                $_.note
        })
    }
    else {
        @("- no cycle has run yet")
    }

    $thesis = "QuantumCylinder should present Problem 3 as a recoverability-aware quantum diffusion benchmark: denoising quality must be judged together with post-selection success probability, diversity retention, and control/resource cost."
    $safeClaim = "Small-scale state-vector experiments support continuous measurement-basis post-selection as a reproducible post-selected toy denoising proxy. The axis-only margin is small, so do not claim hardware advantage, general quantum advantage, or overwhelming continuous-basis superiority."
    $priority = "Autopilot priorities: satisfy Problem 3(a/b/c), add frozen holdout or baseline/collapse table, preserve the 20-seed gate, produce judge-facing figure/table/claim text."

    $lines = @(
        "# Problem 3 Finalist Autopilot Status",
        "",
        ('- generated_at: `{0}`' -f (Get-Date -Format s)),
        ('- mode: `{0}`' -f $Mode),
        ('- branch: `{0}`' -f $branch),
        ('- python: `{0}`' -f $projectPython),
        ('- cycle_minutes: `{0}`' -f $CycleMinutes),
        ('- max_cycles: `{0}` (`0` means run until Ctrl+C)' -f $MaxCycles),
        ('- hermes_max_turns: `{0}`' -f $HermesMaxTurns),
        ('- hermes_attempts_per_cycle: `{0}`' -f $HermesAttempts),
        ('- hermes_heartbeat_seconds: `{0}`' -f $HermesHeartbeatSeconds),
        ('- full_seed_sweep_every: `{0}` (`0` means disabled)' -f $FullSeedSweepEvery),
        ('- run_hours: `{0}` (`0` means disabled)' -f $RunHours),
        ('- stop_at: `{0}`' -f $(Format-Deadline -Deadline $script:StopDeadline)),
        ('- min_remaining_minutes_for_next_cycle: `{0}`' -f $MinRemainingMinutesForNextCycle),
        '- hermes_task: `problem-3-finalist-autopilot`',
        '- loop purpose: `sync -> verify -> evidence improvement -> verify -> optional seed sweep -> record`',
        '- seed summary: `results/problem_3_seed_sweep/seed_sweep_summary.md`',
        '- hybrid toy summary: `results/problem_3_hybrid_diffusion_toy/hybrid_toy_summary.md`',
        '- progress log: `results/problem_3_finalist_autopilot/progress_log.md`',
        '- logs: `logs/problem_3_finalist_autopilot/`',
        "",
        "## Finalist Thesis",
        "",
        $thesis,
        "",
        "## Latest Problem 3 Gate",
        "",
        ('- recommendation: `{0}`' -f $metrics.recommendation),
        ('- total seeds: `{0}`' -f $metrics.total_seeds),
        ('- use_as_main seeds: `{0}`' -f $metrics.use_as_main),
        ('- main_candidate row fraction: `{0}`' -f $metrics.main_fraction),
        ('- median MMD improvement: `{0}`' -f $metrics.mmd_improvement),
        ('- median Wasserstein improvement: `{0}`' -f $metrics.wasserstein_improvement),
        ('- median axis-only score margin: `{0}`' -f $metrics.axis_margin),
        ('- median diversity retention: `{0}`' -f $metrics.diversity),
        ('- median success probability: `{0}`' -f $metrics.success_probability),
        ('- nonpositive axis-margin rows: `{0}`' -f $metrics.nonpositive_axis_rows),
        "",
        "## Hybrid Toy Gate",
        "",
        ('- positive-improvement rows: `{0}`' -f $hybridMetrics.positive_rows),
        ('- median MMD improvement: `{0}`' -f $hybridMetrics.mmd_improvement),
        ('- median Wasserstein improvement: `{0}`' -f $hybridMetrics.wasserstein_improvement),
        ('- median diversity retention: `{0}`' -f $hybridMetrics.diversity),
        ('- median success probability: `{0}`' -f $hybridMetrics.success_probability),
        "",
        "## Recent Cycles",
        ""
    ) + $cycleLines + @(
        "",
        "## Safe Claim Guardrail",
        "",
        $safeClaim,
        "",
        "## Current Evidence Priority",
        "",
        $priority,
        "",
        "## Git Status",
        "",
        '```text'
    ) + $gitStatus + @(
        '```'
    )

    Set-SharedUtf8Text -Path $resolvedPath -Text (($lines -join "`n") + "`n")
    Write-Step "Wrote autopilot status: $resolvedPath"
}

function Invoke-Verification {
    param([string]$Phase)

    if (-not $SkipTests) {
        Write-Step "START: pytest ($Phase)"
        & $projectPython -m pytest --basetemp ".pytest_tmp_p3_finalist_$Phase"
        Assert-LastExitCode "python -m pytest ($Phase)"
        Write-Step "PASS: pytest ($Phase)"
    }
    else {
        Write-Step "SKIP: pytest ($Phase)"
    }

    if (-not $SkipSubmissionQuick) {
        Write-Step "START: submission quick ($Phase)"
        & $projectPython submission/run_all.py --quick
        Assert-LastExitCode "python submission/run_all.py --quick ($Phase)"
        Write-Step "PASS: submission quick ($Phase)"
    }
    else {
        Write-Step "SKIP: submission quick ($Phase)"
    }
}

function Invoke-SeedSweepIfNeeded {
    param([int]$Cycle)

    if ($FullSeedSweepEvery -le 0) {
        return "disabled"
    }

    $summaryPath = Join-Path $repoRoot "results\problem_3_seed_sweep\seed_sweep_summary.md"
    $shouldRun = (-not (Test-Path -LiteralPath $summaryPath)) -or (($Cycle % $FullSeedSweepEvery) -eq 0)
    if (-not $shouldRun) {
        Write-Step "SKIP: full seed sweep this cycle. It runs every $FullSeedSweepEvery cycle(s)."
        return "skipped"
    }

    Write-Step "START: full Problem 3 seed sweep"
    & (Join-Path $PSScriptRoot "run_problem_3_seed_sweep_visible.ps1") `
        -Seeds $Seeds `
        -Python $projectPython `
        -SkipTests
    Assert-LastExitCode "run_problem_3_seed_sweep_visible.ps1"
    Write-Step "PASS: full Problem 3 seed sweep"
    return "ran"
}

function Start-DetachedAutopilot {
    $logRootPath = Resolve-RepoPath -Path $LogRoot
    New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null
    $runId = Get-Date -Format "yyyyMMdd_HHmmss"
    $outerOutLog = Join-Path $logRootPath "$runId-detached-autopilot.out.log"
    $outerErrLog = Join-Path $logRootPath "$runId-detached-autopilot.err.log"
    $pidPath = Join-Path $logRootPath "detached_process.json"

    $childArgs = @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $PSCommandPath,
        "-CycleMinutes", "$CycleMinutes",
        "-MaxCycles", "$MaxCycles",
        "-HermesMaxTurns", "$HermesMaxTurns",
        "-HermesAttempts", "$HermesAttempts",
        "-HermesRetryDelaySeconds", "$HermesRetryDelaySeconds",
        "-HermesHeartbeatSeconds", "$HermesHeartbeatSeconds",
        "-IdleTimeoutMinutes", "$IdleTimeoutMinutes",
        "-FullSeedSweepEvery", "$FullSeedSweepEvery",
        "-RunHours", "$RunHours",
        "-MinRemainingMinutesForNextCycle", "$MinRemainingMinutesForNextCycle",
        "-StatusOutput", $StatusOutput,
        "-ProgressLog", $ProgressLog,
        "-LogRoot", $LogRoot
    )

    if ($StopAt) {
        $childArgs += @("-StopAt", $StopAt)
    }
    $childArgs += @("-SeedList", ($Seeds -join ","))
    if ($Python) {
        $childArgs += @("-Python", $Python)
    }
    if ($KeepDisplayOff) {
        $childArgs += "-KeepDisplayOff"
    }
    if ($AllowNonMainBranch) {
        $childArgs += "-AllowNonMainBranch"
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
    if ($SkipIssueSync) {
        $childArgs += "-SkipIssueSync"
    }
    if ($StatusOnly) {
        $childArgs += "-StatusOnly"
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

    Write-Step "Detached Problem 3 finalist autopilot started with PID $($process.Id)."
    Write-Step "Outer stdout log: $outerOutLog"
    Write-Step "Outer stderr log: $outerErrLog"
    Write-Step "Status: $(Resolve-RepoPath -Path $StatusOutput)"
    Write-Step "Stop with: .\scripts\stop_problem_3_finalist_autopilot.ps1"
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$projectPython = Resolve-ProjectPython -RequestedPython $Python
$watchdog = Join-Path $PSScriptRoot "run_hermes_watchdog.ps1"
if (-not (Test-Path -LiteralPath $watchdog)) {
    throw "Hermes watchdog script not found: $watchdog"
}

$script:CycleResults = @()
$script:StopDeadline = $null
$consoleState = $null

Push-Location $repoRoot
try {
    if ($Detached) {
        Start-DetachedAutopilot
        return
    }

    $consoleState = Disable-QuickEditMode
    Initialize-KeepAwake -DisplayOff:$KeepDisplayOff
    $script:StopDeadline = Resolve-Deadline

    Write-Step "Problem 3 finalist autopilot started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Python: $projectPython"
    Write-Step "Cycle minutes: $CycleMinutes"
    Write-Step "Full seed sweep every: $FullSeedSweepEvery"
    Write-Step "Stop deadline: $(Format-Deadline -Deadline $script:StopDeadline)"
    if ($MaxCycles -eq 0) {
        Write-Step "Max cycles: unlimited until Ctrl+C"
    }
    else {
        Write-Step "Max cycles: $MaxCycles"
    }

    $currentBranch = (git branch --show-current).Trim()
    if ($currentBranch -ne "main" -and -not $AllowNonMainBranch) {
        throw "Current branch is '$currentBranch'. Switch to main or pass -AllowNonMainBranch intentionally."
    }
    if ($CycleMinutes -lt 0) {
        throw "CycleMinutes must be 0 or greater."
    }
    if ($FullSeedSweepEvery -lt 0) {
        throw "FullSeedSweepEvery must be 0 or greater."
    }
    if ($RunHours -lt 0) {
        throw "RunHours must be 0 or greater."
    }
    if ($MinRemainingMinutesForNextCycle -lt 0) {
        throw "MinRemainingMinutesForNextCycle must be 0 or greater."
    }

    if ($StatusOnly) {
        Initialize-ProgressLog -Path $ProgressLog | Out-Null
        Write-AutopilotStatus -Path $StatusOutput -Mode "status-only"
        Write-Step "Status-only mode finished."
        return
    }

    $cycle = 0
    while ($true) {
        if (-not (Test-ShouldStartCycle -Deadline $script:StopDeadline)) {
            Write-Step "Problem 3 finalist autopilot stopped before starting a new cycle."
            break
        }

        $cycle++
        $startedAt = Get-Date
        Write-Step "START: Problem 3 finalist autopilot cycle $cycle"

        $status = "pass"
        $note = "Autopilot cycle completed."
        $seedSweepStatus = "not-started"

        try {
            if (-not $SkipTeamSync) {
                Write-Step "START: team sync"
                & (Join-Path $PSScriptRoot "sync_latest_team_changes.ps1")
                Assert-LastExitCode "sync_latest_team_changes.ps1"
                Write-Step "PASS: team sync"
            }
            else {
                Write-Step "SKIP: team sync"
            }

            Invoke-Verification -Phase "before_cycle_$cycle"

            & $watchdog problem-3-finalist-autopilot `
                -Yolo `
                -MaxTurns $HermesMaxTurns `
                -Attempts $HermesAttempts `
                -RetryDelaySeconds $HermesRetryDelaySeconds `
                -HeartbeatSeconds $HermesHeartbeatSeconds `
                -IdleTimeoutMinutes $IdleTimeoutMinutes `
                -LogRoot $LogRoot `
                -KeepDisplayOff:$KeepDisplayOff
            Assert-LastExitCode "run_hermes_watchdog.ps1 problem-3-finalist-autopilot"

            Invoke-Verification -Phase "after_cycle_$cycle"

            $seedSweepStatus = Invoke-SeedSweepIfNeeded -Cycle $cycle

            if (-not $SkipIssueSync) {
                Write-Step "START: GitHub issue sync"
                & (Join-Path $PSScriptRoot "sync_hackathon_issues.ps1") -Apply
                Assert-LastExitCode "sync_hackathon_issues.ps1 -Apply"
                Write-Step "PASS: GitHub issue sync"
            }
            else {
                Write-Step "SKIP: GitHub issue sync"
            }
        }
        catch {
            $status = "failed"
            $note = $_.Exception.Message
            Write-Step "FAILED: Problem 3 finalist autopilot cycle $cycle"
            Write-Host $note -ForegroundColor Yellow
        }

        $endedAt = Get-Date
        $duration = New-TimeSpan -Start $startedAt -End $endedAt
        $changeLines = Get-CurrentChangeLines
        $changedFiles = if ($changeLines.Count -eq 0 -or ($changeLines.Count -eq 1 -and $changeLines[0] -eq "none")) {
            "none"
        }
        else {
            ($changeLines | Select-Object -First 12) -join "; "
        }

        $script:CycleResults += [pscustomobject]@{
            cycle = $cycle
            status = $status
            started_at = $startedAt.ToString("s")
            finished_at = $endedAt.ToString("s")
            duration = (Format-RunDuration -Duration $duration)
            note = $note
            seed_sweep = $seedSweepStatus
            changed_files = $changedFiles
        }

        Add-ProgressLogEntry -Path $ProgressLog -CycleResult $script:CycleResults[-1] -ChangeLines $changeLines
        Write-AutopilotStatus -Path $StatusOutput -Mode "continuous"
        Write-Step "END: Problem 3 finalist autopilot cycle $cycle with status $status"

        if ($MaxCycles -gt 0 -and $cycle -ge $MaxCycles) {
            Write-Step "Reached MaxCycles=$MaxCycles. Problem 3 finalist autopilot finished."
            break
        }

        if (-not (Test-ShouldStartCycle -Deadline $script:StopDeadline)) {
            Write-Step "Problem 3 finalist autopilot reached its overnight stop condition."
            break
        }

        if ($CycleMinutes -eq 0) {
            Write-Step "Starting next cycle immediately. Press Ctrl+C to stop."
            continue
        }

        $sleepSeconds = $CycleMinutes * 60
        if ($null -ne $script:StopDeadline) {
            $remaining = Get-RemainingUntilDeadline -Deadline $script:StopDeadline
            $maxSleepSeconds = [math]::Max(0, [int]$remaining.TotalSeconds)
            if ($sleepSeconds -gt $maxSleepSeconds) {
                $sleepSeconds = $maxSleepSeconds
            }
        }
        if ($sleepSeconds -le 0) {
            Write-Step "Stop deadline reached before sleep. Autopilot finished."
            break
        }
        Write-Step "Sleeping for $([math]::Round($sleepSeconds / 60, 2)) minutes before next cycle. Press Ctrl+C to stop."
        Start-Sleep -Seconds $sleepSeconds
    }
}
finally {
    Clear-KeepAwake
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
}
