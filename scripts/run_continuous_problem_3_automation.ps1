param(
    [int]$CycleMinutes = 90,
    [int]$MaxCycles = 0,
    [int]$HermesMaxTurns = 420,
    [int]$HermesAttempts = 2,
    [int]$IdleTimeoutMinutes = 45,
    [string]$StatusOutput = "results/continuous_problem_3/latest_status.md",
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
    $seedSummary = Get-FileTextIfExists -Path $seedSummaryPath

    $recommendation = Get-MarkdownMetric -Text $seedSummary -Label "Main-claim recommendation"
    $totalSeeds = Get-MarkdownMetric -Text $seedSummary -Label "Total seeds"
    $useAsMain = Get-MarkdownMetric -Text $seedSummary -Label "use_as_main"
    $mainFraction = Get-MarkdownMetric -Text $seedSummary -Label "main_candidate row fraction"
    $mmdImprovement = Get-MarkdownMetric -Text $seedSummary -Label "continuous_mmd_improvement"
    $wassersteinImprovement = Get-MarkdownMetric -Text $seedSummary -Label "continuous_wasserstein_improvement"
    $axisMargin = Get-MarkdownMetric -Text $seedSummary -Label "continuous_score_minus_axis_score"
    $diversity = Get-MarkdownMetric -Text $seedSummary -Label "continuous_diversity_retention"
    $successProbability = Get-MarkdownMetric -Text $seedSummary -Label "continuous_mean_success_probability"

    $branch = (git branch --show-current).Trim()
    $gitStatus = @(git status --short --branch)
    $cycleLines = if ($script:CycleResults.Count -gt 0) {
        @($script:CycleResults | Select-Object -Last 12 | ForEach-Object {
            "- cycle {0}: `{1}` started `{2}`, duration `{3}` - {4}" -f `
                $_.cycle, `
                $_.status, `
                $_.started_at, `
                $_.duration, `
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
        '- loop purpose: `experiment -> analyze -> decide -> apply -> verify -> record`',
        '- seed summary: `results/problem_3_seed_sweep/seed_sweep_summary.md`',
        '- default summary: `results/problem_3_continuous_denoising/problem_3_summary.md`',
        '- logs: `logs/continuous_problem_3/`',
        "",
        "## Latest Problem 3 Gate",
        "",
        ('- recommendation: `{0}`' -f $recommendation),
        ('- total seeds: `{0}`' -f $totalSeeds),
        ('- use_as_main seeds: `{0}`' -f $useAsMain),
        ('- main_candidate row fraction: `{0}`' -f $mainFraction),
        ('- median MMD improvement: `{0}`' -f $mmdImprovement),
        ('- median Wasserstein improvement: `{0}`' -f $wassersteinImprovement),
        ('- median axis-only score margin: `{0}`' -f $axisMargin),
        ('- median diversity retention: `{0}`' -f $diversity),
        ('- median success probability: `{0}`' -f $successProbability),
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

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$watchdog = Join-Path $PSScriptRoot "run_hermes_watchdog.ps1"
if (-not (Test-Path -LiteralPath $watchdog)) {
    throw "Hermes watchdog script not found: $watchdog"
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

    if ($StatusOnly) {
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
            & $watchdog continuous-p3-improvement `
                -Yolo `
                -MaxTurns $HermesMaxTurns `
                -Attempts $HermesAttempts `
                -IdleTimeoutMinutes $IdleTimeoutMinutes `
                -LogRoot "logs/continuous_problem_3" `
                -KeepDisplayOff:$KeepDisplayOff
            Assert-LastExitCode "run_hermes_watchdog.ps1 continuous-p3-improvement"
        }
        catch {
            $status = "failed"
            $note = $_.Exception.Message
            Write-Step "FAILED: continuous Problem 3 cycle $cycle"
            Write-Host $note -ForegroundColor Yellow
        }

        $endedAt = Get-Date
        $duration = New-TimeSpan -Start $startedAt -End $endedAt
        $script:CycleResults += [pscustomobject]@{
            cycle = $cycle
            status = $status
            started_at = $startedAt.ToString("s")
            finished_at = $endedAt.ToString("s")
            duration = (Format-RunDuration -Duration $duration)
            note = $note
        }

        Write-ContinuousStatus -Path $StatusOutput -Mode "continuous"
        Write-Step "END: continuous Problem 3 cycle $cycle with status $status"

        if ($MaxCycles -gt 0 -and $cycle -ge $MaxCycles) {
            Write-Step "Reached MaxCycles=$MaxCycles. Continuous automation finished."
            break
        }

        $sleepSeconds = [Math]::Max(1, $CycleMinutes * 60)
        Write-Step "Sleeping for $CycleMinutes minutes before next cycle. Press Ctrl+C to stop."
        Start-Sleep -Seconds $sleepSeconds
    }
}
finally {
    Clear-KeepAwake
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
}
