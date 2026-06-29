param(
    [int]$CycleMinutes = 0,
    [int]$MaxCycles = 0,
    [int]$HermesMaxTurns = 420,
    [int]$HermesAttempts = 2,
    [int]$HermesRetryDelaySeconds = 0,
    [int]$HermesHeartbeatSeconds = 10,
    [int]$IdleTimeoutMinutes = 45,
    [string]$StatusOutput = "results/continuous_problem_3/latest_status.md",
    [string]$ProgressLog = "results/continuous_problem_3/progress_log.md",
    [switch]$UseWatchdog,
    [switch]$KeepDisplayOff,
    [switch]$AllowNonMainBranch,
    [switch]$StatusOnly
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

function Initialize-KeepAwake {
    param([switch]$DisplayOff)

    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderAutomation.PowerManagement").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderAutomation {
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

    [QuantumCylinderAutomation.PowerManagement]::SetThreadExecutionState([uint32]$flags) | Out-Null
}

function Clear-KeepAwake {
    if (([System.Management.Automation.PSTypeName]"QuantumCylinderAutomation.PowerManagement").Type) {
        [QuantumCylinderAutomation.PowerManagement]::SetThreadExecutionState([uint32]2147483648) | Out-Null
    }
}

function Disable-QuickEditMode {
    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderAutomation.ConsoleMode").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderAutomation {
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

    $handle = [QuantumCylinderAutomation.ConsoleMode]::GetStdHandle($STD_INPUT_HANDLE)
    if ($handle -eq [IntPtr]::Zero -or $handle.ToInt64() -eq -1) {
        return $null
    }

    $mode = 0
    if (-not [QuantumCylinderAutomation.ConsoleMode]::GetConsoleMode($handle, [ref]$mode)) {
        return $null
    }

    $newMode = ($mode -bor $ENABLE_EXTENDED_FLAGS) -band (-bnot $ENABLE_QUICK_EDIT_MODE)
    [QuantumCylinderAutomation.ConsoleMode]::SetConsoleMode($handle, $newMode) | Out-Null

    return @{
        Handle = $handle
        Mode = $mode
    }
}

function Restore-ConsoleMode {
    param($ConsoleState)

    if ($ConsoleState -and ([System.Management.Automation.PSTypeName]"QuantumCylinderAutomation.ConsoleMode").Type) {
        [QuantumCylinderAutomation.ConsoleMode]::SetConsoleMode($ConsoleState.Handle, $ConsoleState.Mode) | Out-Null
    }
}

function Format-RunDuration {
    param([TimeSpan]$Duration)
    return ("{0:00}:{1:00}:{2:00}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds)
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

function Resolve-RepoPath {
    param([string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return Join-Path $repoRoot $Path
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
            '# Continuous Problem 3 Progress Log',
            "",
            'This generated log records each automation cycle so the team can see progress while the loop is running.',
            "",
            '- source status: generated under `results/`, ignored by Git',
            '- main status file: `results/continuous_problem_3/latest_status.md`',
            '- detailed Hermes logs: `logs/continuous_problem_3/`',
            ""
        )
        $lines -join "`n" | Set-Content -LiteralPath $resolvedPath -Encoding UTF8
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
    ) + $changeMarkdown + @(
        ""
    )

    Add-Content -LiteralPath $resolvedPath -Value ($entry -join "`n") -Encoding UTF8
    Write-Step "Appended progress log: $resolvedPath"
}

function Write-ContinuousStatus {
    param(
        [string]$Path,
        [string]$Mode
    )

    $resolvedPath = if ([System.IO.Path]::IsPathRooted($Path)) {
        $Path
    }
    else {
        Join-Path $repoRoot $Path
    }
    $statusDir = Split-Path -Parent $resolvedPath
    New-Item -ItemType Directory -Force -Path $statusDir | Out-Null

    $seedSummaryPath = Join-Path $repoRoot "results\problem_3_seed_sweep\seed_sweep_summary.md"
    $p3SummaryPath = Join-Path $repoRoot "results\problem_3_continuous_denoising\problem_3_summary.md"
    $metrics = Get-Problem3Metrics

    $branch = (git branch --show-current).Trim()
    $gitStatus = @(git status --short --branch)
    $cycleLines = if ($script:CycleResults.Count -gt 0) {
        @($script:CycleResults | Select-Object -Last 12 | ForEach-Object {
            "- cycle {0}: `{1}` started `{2}`, duration `{3}`, changes `{4}` - {5}" -f `
                $_.cycle, `
                $_.status, `
                $_.started_at, `
                $_.duration, `
                $_.changed_files, `
                $_.note
        })
    }
    else {
        @("- no cycle has run yet")
    }

    $safeClaim = "Small-scale state-vector experiments support using the Problem 3 continuous measurement-basis search as the main toy denoising proxy: it improves baseline MMD/Wasserstein metrics across the 20-seed sweep. Because the axis-only score margin is small, this should be claimed only as a reproducible post-selected proxy improvement, not as hardware advantage or general quantum advantage."

    $lines = @(
        "# Continuous Problem 3 Automation Status",
        "",
        ('- generated_at: `{0}`' -f (Get-Date -Format s)),
        ('- mode: `{0}`' -f $Mode),
        ('- branch: `{0}`' -f $branch),
        ('- cycle_minutes: `{0}`' -f $CycleMinutes),
        ('- max_cycles: `{0}` (`0` means run until Ctrl+C)' -f $MaxCycles),
        ('- hermes_max_turns: `{0}`' -f $HermesMaxTurns),
        ('- hermes_attempts_per_cycle: `{0}`' -f $HermesAttempts),
        ('- hermes_retry_delay_seconds: `{0}`' -f $HermesRetryDelaySeconds),
        ('- hermes_heartbeat_seconds: `{0}`' -f $HermesHeartbeatSeconds),
        ('- hermes_run_mode: `{0}`' -f $(if ($UseWatchdog) { "watchdog" } else { "attached" })),
        '- loop purpose: `experiment -> analyze -> decide -> apply -> verify -> record`',
        '- seed summary: `results/problem_3_seed_sweep/seed_sweep_summary.md`',
        '- default summary: `results/problem_3_continuous_denoising/problem_3_summary.md`',
        ('- progress log: `{0}`' -f $ProgressLog),
        '- logs: `logs/continuous_problem_3/`',
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
        "",
        "## Recent Cycles",
        ""
    ) + $cycleLines + @(
        "",
        "## Safe Claim Guardrail",
        "",
        $safeClaim,
        "",
        "## Git Status",
        "",
        '```text'
    ) + $gitStatus + @(
        '```'
    )

    if (-not (Test-Path -LiteralPath $seedSummaryPath)) {
        $lines += @("", "Warning: seed sweep summary was not found.")
    }
    if (-not (Test-Path -LiteralPath $p3SummaryPath)) {
        $lines += @("", "Warning: default Problem 3 summary was not found.")
    }

    $lines -join "`n" | Set-Content -LiteralPath $resolvedPath -Encoding UTF8
    Write-Step "Wrote continuous status: $resolvedPath"
}

function Write-HermesState {
    param(
        [string]$Path,
        [hashtable]$State
    )

    $stateDir = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
    $State["updated_at"] = (Get-Date).ToString("s")
    $State | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Invoke-AttachedHermesCycle {
    param([int]$Cycle)

    $logRootPath = Join-Path $repoRoot "logs\continuous_problem_3"
    $statePath = Join-Path $logRootPath "latest_state.json"
    New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null

    for ($attempt = 1; $attempt -le $HermesAttempts; $attempt++) {
        $runId = Get-Date -Format "yyyyMMdd_HHmmss"
        $logPath = Join-Path $logRootPath "$runId-continuous-p3-improvement-cycle-$Cycle-attempt-$attempt.log"
        $state = @{
            status = "running"
            task = "continuous-p3-improvement"
            cycle = $Cycle
            attempt = $attempt
            attempts = $HermesAttempts
            log = $logPath
            exit_code = $null
            run_mode = "attached"
        }
        Write-HermesState -Path $statePath -State $state

        $startedAt = Get-Date
        $transcriptStarted = $false
        $exitCode = 1
        $failureMessage = ""

        Write-Step "Attached Hermes attempt $attempt/$HermesAttempts started. Live output is shown in this PowerShell."
        Add-Content -LiteralPath $logPath -Encoding UTF8 -Value "[$(Get-Date -Format "s")] Attached Hermes attempt $attempt/$HermesAttempts"

        try {
            try {
                Start-Transcript -Path $logPath -Append -ErrorAction Stop | Out-Null
                $transcriptStarted = $true
            }
            catch {
                $failureMessage = "Transcript unavailable: $($_.Exception.Message)"
                Write-Step $failureMessage
                Add-Content -LiteralPath $logPath -Encoding UTF8 -Value "[$(Get-Date -Format "s")] $failureMessage"
            }

            $global:LASTEXITCODE = 0
            & $invokeScript continuous-p3-improvement -Yolo -MaxTurns $HermesMaxTurns
            $exitCode = $LASTEXITCODE
            if ($null -eq $exitCode) {
                $exitCode = 0
            }
        }
        catch {
            $failureMessage = $_.Exception.Message
            $exitCode = if ($LASTEXITCODE -ne 0) { $LASTEXITCODE } else { 1 }
            Write-Step "Attached Hermes attempt failed: $failureMessage"
            Add-Content -LiteralPath $logPath -Encoding UTF8 -Value "[$(Get-Date -Format "s")] ERROR: $failureMessage"
        }
        finally {
            if ($transcriptStarted) {
                try {
                    Stop-Transcript | Out-Null
                }
                catch {
                    Write-Step "Could not stop transcript cleanly: $($_.Exception.Message)"
                }
            }
        }

        $duration = New-TimeSpan -Start $startedAt -End (Get-Date)
        $state["status"] = if ($exitCode -eq 0) { "completed" } else { "failed" }
        $state["exit_code"] = $exitCode
        $state["duration"] = Format-RunDuration -Duration $duration
        if ($failureMessage) {
            $state["message"] = $failureMessage
        }
        Write-HermesState -Path $statePath -State $state

        Write-Step "Attached Hermes attempt $attempt/$HermesAttempts finished with exit code $exitCode."
        if ($exitCode -eq 0) {
            $global:LASTEXITCODE = 0
            return
        }

        if ($attempt -lt $HermesAttempts) {
            Write-Step "Retrying in $HermesRetryDelaySeconds seconds."
            Start-Sleep -Seconds $HermesRetryDelaySeconds
        }
    }

    $global:LASTEXITCODE = 1
    throw "Attached Hermes failed after $HermesAttempts attempts. See logs: $logRootPath"
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$watchdog = Join-Path $PSScriptRoot "run_hermes_watchdog.ps1"
if (-not (Test-Path -LiteralPath $watchdog)) {
    throw "Hermes watchdog script not found: $watchdog"
}
$invokeScript = Join-Path $PSScriptRoot "invoke_hermes_task.ps1"
if (-not (Test-Path -LiteralPath $invokeScript)) {
    throw "Hermes invoke script not found: $invokeScript"
}

$script:CycleResults = @()
$consoleState = $null

Push-Location $repoRoot
try {
    $consoleState = Disable-QuickEditMode
    Initialize-KeepAwake -DisplayOff:$KeepDisplayOff

    Write-Step "Continuous Problem 3 automation started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Cycle minutes: $CycleMinutes"
    Write-Step "Hermes run mode: $(if ($UseWatchdog) { "watchdog" } else { "attached" })"
    Write-Step "Hermes retry delay seconds: $HermesRetryDelaySeconds"
    Write-Step "Hermes heartbeat seconds: $HermesHeartbeatSeconds"
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
    if ($HermesRetryDelaySeconds -lt 0) {
        throw "HermesRetryDelaySeconds must be 0 or greater."
    }
    if ($HermesHeartbeatSeconds -lt 1) {
        throw "HermesHeartbeatSeconds must be 1 or greater."
    }

    if ($StatusOnly) {
        Initialize-ProgressLog -Path $ProgressLog | Out-Null
        Write-ContinuousStatus -Path $StatusOutput -Mode "status-only"
        Write-Step "Status-only mode finished."
        return
    }

    $cycle = 0
    while ($true) {
        $cycle++
        $startedAt = Get-Date
        Write-Step "START: continuous Problem 3 cycle $cycle"

        $status = "pass"
        $note = "Hermes cycle completed."
        try {
            if ($UseWatchdog) {
                & $watchdog continuous-p3-improvement `
                    -Yolo `
                    -MaxTurns $HermesMaxTurns `
                    -Attempts $HermesAttempts `
                    -RetryDelaySeconds $HermesRetryDelaySeconds `
                    -HeartbeatSeconds $HermesHeartbeatSeconds `
                    -IdleTimeoutMinutes $IdleTimeoutMinutes `
                    -LogRoot "logs/continuous_problem_3" `
                    -KeepDisplayOff:$KeepDisplayOff
                Assert-LastExitCode "run_hermes_watchdog.ps1 continuous-p3-improvement"
            }
            else {
                Invoke-AttachedHermesCycle -Cycle $cycle
            }
        }
        catch {
            $status = "failed"
            $note = $_.Exception.Message
            Write-Step "FAILED: continuous Problem 3 cycle $cycle"
            Write-Host $note -ForegroundColor Yellow
        }

        $endedAt = Get-Date
        $duration = New-TimeSpan -Start $startedAt -End $endedAt
        $changeLines = Get-CurrentChangeLines
        $changedFiles = if ($changeLines.Count -eq 0 -or ($changeLines.Count -eq 1 -and $changeLines[0] -eq "none")) {
            "none"
        }
        else {
            ($changeLines | Select-Object -First 8) -join "; "
        }
        $script:CycleResults += [pscustomobject]@{
            cycle = $cycle
            status = $status
            started_at = $startedAt.ToString("s")
            finished_at = $endedAt.ToString("s")
            duration = (Format-RunDuration -Duration $duration)
            note = $note
            changed_files = $changedFiles
        }

        Add-ProgressLogEntry -Path $ProgressLog -CycleResult $script:CycleResults[-1] -ChangeLines $changeLines
        Write-ContinuousStatus -Path $StatusOutput -Mode "continuous"
        Write-Step "END: continuous Problem 3 cycle $cycle with status $status"

        if ($MaxCycles -gt 0 -and $cycle -ge $MaxCycles) {
            Write-Step "Reached MaxCycles=$MaxCycles. Continuous automation finished."
            break
        }

        if ($CycleMinutes -eq 0) {
            Write-Step "Starting next cycle immediately. Press Ctrl+C to stop."
            continue
        }

        $sleepSeconds = $CycleMinutes * 60
        Write-Step "Sleeping for $CycleMinutes minutes before next cycle. Press Ctrl+C to stop."
        Start-Sleep -Seconds $sleepSeconds
    }
}
finally {
    Clear-KeepAwake
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
}
