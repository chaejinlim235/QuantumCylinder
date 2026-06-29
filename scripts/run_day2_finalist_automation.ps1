param(
    [int]$CycleMinutes = 0,
    [int]$MaxCycles = 0,
    [int]$HermesMaxTurns = 520,
    [int]$HermesAttempts = 2,
    [int]$HermesRetryDelaySeconds = 0,
    [int]$HermesHeartbeatSeconds = 10,
    [int]$IdleTimeoutMinutes = 60,
    [string]$StatusOutput = "results/day2_finalist_automation/latest_status.md",
    [string]$ProgressLog = "results/day2_finalist_automation/progress_log.md",
    [string]$LogRoot = "logs/day2_finalist_automation",
    [switch]$UseWatchdog,
    [switch]$KeepDisplayOff,
    [switch]$AllowNonMainBranch,
    [switch]$SkipTeamSync,
    [switch]$SkipTests,
    [switch]$SkipSubmissionQuick,
    [switch]$ApplyIssueSync,
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

    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderDay2.PowerManagement").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderDay2 {
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

    [QuantumCylinderDay2.PowerManagement]::SetThreadExecutionState([uint32]$flags) | Out-Null
}

function Clear-KeepAwake {
    if (([System.Management.Automation.PSTypeName]"QuantumCylinderDay2.PowerManagement").Type) {
        [QuantumCylinderDay2.PowerManagement]::SetThreadExecutionState([uint32]2147483648) | Out-Null
    }
}

function Disable-QuickEditMode {
    if (-not ([System.Management.Automation.PSTypeName]"QuantumCylinderDay2.ConsoleMode").Type) {
        Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace QuantumCylinderDay2 {
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

    $handle = [QuantumCylinderDay2.ConsoleMode]::GetStdHandle($STD_INPUT_HANDLE)
    if ($handle -eq [IntPtr]::Zero -or $handle.ToInt64() -eq -1) {
        return $null
    }

    $mode = 0
    if (-not [QuantumCylinderDay2.ConsoleMode]::GetConsoleMode($handle, [ref]$mode)) {
        return $null
    }

    $newMode = ($mode -bor $ENABLE_EXTENDED_FLAGS) -band (-bnot $ENABLE_QUICK_EDIT_MODE)
    [QuantumCylinderDay2.ConsoleMode]::SetConsoleMode($handle, $newMode) | Out-Null

    return @{
        Handle = $handle
        Mode = $mode
    }
}

function Restore-ConsoleMode {
    param($ConsoleState)

    if ($ConsoleState -and ([System.Management.Automation.PSTypeName]"QuantumCylinderDay2.ConsoleMode").Type) {
        [QuantumCylinderDay2.ConsoleMode]::SetConsoleMode($ConsoleState.Handle, $ConsoleState.Mode) | Out-Null
    }
}

function Format-RunDuration {
    param([TimeSpan]$Duration)
    return ("{0:00}:{1:00}:{2:00}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds)
}

function Resolve-RepoPath {
    param([string]$Path)
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return Join-Path $repoRoot $Path
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
            "# Day 2 Finalist Automation Progress Log",
            "",
            "This generated log records each finalist-defense automation cycle.",
            "",
            '- source status: generated under `results/`, ignored by Git',
            '- main status file: `results/day2_finalist_automation/latest_status.md`',
            '- detailed Hermes logs: `logs/day2_finalist_automation/`',
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
    ) + $changeMarkdown + @("")

    Add-Content -LiteralPath $resolvedPath -Value ($entry -join "`n") -Encoding UTF8
    Write-Step "Appended progress log: $resolvedPath"
}

function Write-Day2Status {
    param(
        [string]$Path,
        [string]$Mode
    )

    $resolvedPath = Resolve-RepoPath -Path $Path
    $statusDir = Split-Path -Parent $resolvedPath
    New-Item -ItemType Directory -Force -Path $statusDir | Out-Null

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

    $thesis = "QuantumCylinder should be framed as a recoverability-aware quantum diffusion benchmark: compare random-unitary and Hamiltonian projected diffusion under the same fidelity metrics, then evaluate continuous measurement-basis post-selection by recoverability, success probability, diversity retention, and control/resource cost."
    $safeClaim = "Claim only a reproducible small-scale post-selected proxy improvement. Do not claim hardware advantage, broad quantum advantage, or an overwhelming axis-only advantage."
    $priority = "Next evidence priorities: frozen-parameter holdout; identity/axis-only/continuous/collapse baseline table; random-unitary angle ablation; one 2x2 killer figure; judge-facing summary."

    $lines = @(
        "# Day 2 Finalist Automation Status",
        "",
        ('- generated_at: `{0}`' -f (Get-Date -Format s)),
        ('- mode: `{0}`' -f $Mode),
        ('- branch: `{0}`' -f $branch),
        ('- cycle_minutes: `{0}`' -f $CycleMinutes),
        ('- max_cycles: `{0}` (`0` means run until Ctrl+C)' -f $MaxCycles),
        ('- hermes_max_turns: `{0}`' -f $HermesMaxTurns),
        ('- hermes_attempts_per_cycle: `{0}`' -f $HermesAttempts),
        ('- hermes_run_mode: `{0}`' -f $(if ($UseWatchdog) { "watchdog" } else { "attached" })),
        '- task: `p3-defense-evidence`',
        '- loop purpose: `sync -> verify -> build judge-defense evidence -> verify -> record`',
        '- seed summary: `results/problem_3_seed_sweep/seed_sweep_summary.md`',
        ('- progress log: `{0}`' -f $ProgressLog),
        ('- logs: `{0}`' -f $LogRoot),
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
        "## Recent Cycles",
        ""
    ) + $cycleLines + @(
        "",
        "## Safe Claim Guardrail",
        "",
        $safeClaim,
        "",
        "## Evidence Priority",
        "",
        $priority,
        "",
        "## Git Status",
        "",
        '```text'
    ) + $gitStatus + @(
        '```'
    )

    $lines -join "`n" | Set-Content -LiteralPath $resolvedPath -Encoding UTF8
    Write-Step "Wrote Day 2 status: $resolvedPath"
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

function Invoke-Day2HermesAttached {
    param([int]$Cycle)

    $logRootPath = Resolve-RepoPath -Path $LogRoot
    $statePath = Join-Path $logRootPath "latest_state.json"
    New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null

    for ($attempt = 1; $attempt -le $HermesAttempts; $attempt++) {
        $runId = Get-Date -Format "yyyyMMdd_HHmmss"
        $logPath = Join-Path $logRootPath "$runId-p3-defense-evidence-cycle-$Cycle-attempt-$attempt.log"
        $state = @{
            status = "running"
            task = "p3-defense-evidence"
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

        Write-Step "Attached Hermes finalist-defense attempt $attempt/$HermesAttempts started. Live output is shown in this PowerShell."
        Add-Content -LiteralPath $logPath -Encoding UTF8 -Value "[$(Get-Date -Format "s")] Attached Hermes p3-defense-evidence attempt $attempt/$HermesAttempts"

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
            & $invokeScript p3-defense-evidence -Yolo -MaxTurns $HermesMaxTurns
            $exitCode = $LASTEXITCODE
            if ($null -eq $exitCode) {
                $exitCode = 0
            }
        }
        catch {
            $failureMessage = $_.Exception.Message
            $exitCode = if ($LASTEXITCODE -ne 0) { $LASTEXITCODE } else { 1 }
            Write-Step "Attached Hermes finalist-defense attempt failed: $failureMessage"
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

        Write-Step "Attached Hermes finalist-defense attempt $attempt/$HermesAttempts finished with exit code $exitCode."
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
    throw "Attached Hermes p3-defense-evidence failed after $HermesAttempts attempts. See logs: $LogRoot"
}

function Invoke-Verification {
    param([string]$Phase)

    if (-not $SkipTests) {
        Write-Step "START: pytest ($Phase)"
        python -m pytest --basetemp ".pytest_tmp_day2_finalist_$Phase"
        Assert-LastExitCode "python -m pytest ($Phase)"
        Write-Step "PASS: pytest ($Phase)"
    }
    else {
        Write-Step "SKIP: pytest ($Phase)"
    }

    if (-not $SkipSubmissionQuick) {
        Write-Step "START: submission quick ($Phase)"
        python submission/run_all.py --quick
        Assert-LastExitCode "python submission/run_all.py --quick ($Phase)"
        Write-Step "PASS: submission quick ($Phase)"
    }
    else {
        Write-Step "SKIP: submission quick ($Phase)"
    }
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$watchdog = Join-Path $PSScriptRoot "run_hermes_watchdog.ps1"
$invokeScript = Join-Path $PSScriptRoot "invoke_hermes_task.ps1"
if (-not (Test-Path -LiteralPath $watchdog)) {
    throw "Hermes watchdog script not found: $watchdog"
}
if (-not (Test-Path -LiteralPath $invokeScript)) {
    throw "Hermes invoke script not found: $invokeScript"
}

$script:CycleResults = @()
$consoleState = $null

Push-Location $repoRoot
try {
    $consoleState = Disable-QuickEditMode
    Initialize-KeepAwake -DisplayOff:$KeepDisplayOff

    Write-Step "Day 2 finalist automation started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Cycle minutes: $CycleMinutes"
    Write-Step "Hermes run mode: $(if ($UseWatchdog) { "watchdog" } else { "attached" })"
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
        Write-Day2Status -Path $StatusOutput -Mode "status-only"
        Write-Step "Status-only mode finished."
        return
    }

    $cycle = 0
    while ($true) {
        $cycle++
        $startedAt = Get-Date
        Write-Step "START: Day 2 finalist-defense cycle $cycle"

        $status = "pass"
        $note = "Finalist-defense cycle completed."
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

            if ($UseWatchdog) {
                & $watchdog p3-defense-evidence `
                    -Yolo `
                    -MaxTurns $HermesMaxTurns `
                    -Attempts $HermesAttempts `
                    -RetryDelaySeconds $HermesRetryDelaySeconds `
                    -HeartbeatSeconds $HermesHeartbeatSeconds `
                    -IdleTimeoutMinutes $IdleTimeoutMinutes `
                    -LogRoot $LogRoot `
                    -KeepDisplayOff:$KeepDisplayOff
                Assert-LastExitCode "run_hermes_watchdog.ps1 p3-defense-evidence"
            }
            else {
                Invoke-Day2HermesAttached -Cycle $cycle
            }

            Invoke-Verification -Phase "after_cycle_$cycle"

            if ($ApplyIssueSync) {
                Write-Step "START: GitHub issue sync"
                & (Join-Path $PSScriptRoot "sync_hackathon_issues.ps1") -Apply
                Assert-LastExitCode "sync_hackathon_issues.ps1 -Apply"
                Write-Step "PASS: GitHub issue sync"
            }
        }
        catch {
            $status = "failed"
            $note = $_.Exception.Message
            Write-Step "FAILED: Day 2 finalist-defense cycle $cycle"
            Write-Host $note -ForegroundColor Yellow
        }

        $endedAt = Get-Date
        $duration = New-TimeSpan -Start $startedAt -End $endedAt
        $changeLines = Get-CurrentChangeLines
        $changedFiles = if ($changeLines.Count -eq 0 -or ($changeLines.Count -eq 1 -and $changeLines[0] -eq "none")) {
            "none"
        }
        else {
            ($changeLines | Select-Object -First 10) -join "; "
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
        Write-Day2Status -Path $StatusOutput -Mode "continuous"
        Write-Step "END: Day 2 finalist-defense cycle $cycle with status $status"

        if ($MaxCycles -gt 0 -and $cycle -ge $MaxCycles) {
            Write-Step "Reached MaxCycles=$MaxCycles. Day 2 finalist automation finished."
            break
        }

        if ($CycleMinutes -eq 0) {
            Write-Step "Starting next Day 2 finalist-defense cycle immediately. Press Ctrl+C to stop."
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
