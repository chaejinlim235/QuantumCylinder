param(
    [int[]]$Seeds = (1..20),
    [string]$Python = "",
    [string]$StatusOutput = "results/final_automation/latest_status.md",
    [int]$HermesMaxTurns = 360,
    [int]$HermesAttempts = 3,
    [switch]$SkipTeamSync,
    [switch]$SkipQuantitativeEvaluation,
    [switch]$SkipFinalPipeline,
    [switch]$SkipIssueSync,
    [switch]$SkipHermesOnFailure,
    [switch]$KeepDisplayOff,
    [switch]$AllowNonMainBranch
)

$ErrorActionPreference = "Stop"

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

function Assert-LastExitCode {
    param([string]$CommandName)

    if ($LASTEXITCODE -ne 0) {
        throw "$CommandName failed with exit code $LASTEXITCODE"
    }
}

function Add-StepResult {
    param(
        [string]$Name,
        [string]$Status,
        [string]$Note = ""
    )

    $script:StepResults += [pscustomobject]@{
        name = $Name
        status = $Status
        note = $Note
    }
}

function Invoke-HermesFixLoop {
    $watchdog = Join-Path $PSScriptRoot "run_hermes_watchdog.ps1"
    if (-not (Test-Path -LiteralPath $watchdog)) {
        throw "Hermes watchdog script not found: $watchdog"
    }

    Write-Step "Starting Hermes self-fix loop after a failed automation step."
    & $watchdog final-sync-fix `
        -Yolo `
        -MaxTurns $HermesMaxTurns `
        -Attempts $HermesAttempts `
        -IdleTimeoutMinutes 45 `
        -KeepDisplayOff:$KeepDisplayOff
    Assert-LastExitCode "run_hermes_watchdog.ps1 final-sync-fix"
}

function Invoke-AutomationStep {
    param(
        [string]$Name,
        [scriptblock]$Action
    )

    Write-Step "START: $Name"
    try {
        & $Action
        Add-StepResult -Name $Name -Status "pass"
        Write-Step "PASS: $Name"
    }
    catch {
        $firstError = $_.Exception.Message
        Add-StepResult -Name $Name -Status "failed-first" -Note $firstError
        Write-Step "FAILED: $Name"
        Write-Host $firstError -ForegroundColor Yellow

        if ($SkipHermesOnFailure) {
            throw
        }

        Invoke-HermesFixLoop

        Write-Step "RETRY: $Name"
        & $Action
        Add-StepResult -Name "$Name retry" -Status "pass" -Note "Passed after Hermes self-fix loop."
        Write-Step "PASS AFTER RETRY: $Name"
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

function Write-FinalStatus {
    param([string]$Path)

    $resolvedPath = if ([System.IO.Path]::IsPathRooted($Path)) {
        $Path
    }
    else {
        Join-Path $repoRoot $Path
    }
    $statusDir = Split-Path -Parent $resolvedPath
    New-Item -ItemType Directory -Force -Path $statusDir | Out-Null

    $seedSummaryPath = Join-Path $repoRoot "results\problem_3_seed_sweep\seed_sweep_summary.md"
    $submissionSummaryPath = Join-Path $repoRoot "results\submission_simple\SUMMARY.md"
    $quantIndexPath = Join-Path $repoRoot "results\quantitative_evaluation\QUANTITATIVE_EVALUATION_INDEX.md"

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
    $stepLines = @($script:StepResults | ForEach-Object {
        $note = if ($_.note) { " - $($_.note)" } else { "" }
        '- {0}: `{1}`{2}' -f $_.name, $_.status, $note
    })

    $safeClaim = "Small-scale state-vector experiments support using the Problem 3 continuous measurement-basis search as the main toy denoising proxy: it improves baseline MMD/Wasserstein metrics across the 20-seed sweep. Because the axis-only score margin is small, this should be claimed only as a reproducible post-selected proxy improvement, not as hardware advantage or general quantum advantage."

    $lines = @(
        "# Final Competition Automation Status",
        "",
        ('- generated_at: `{0}`' -f (Get-Date -Format s)),
        ('- branch: `{0}`' -f $branch),
        ('- python: `{0}`' -f $projectPython),
        '- seed summary: `results/problem_3_seed_sweep/seed_sweep_summary.md`',
        '- submission summary: `results/submission_simple/SUMMARY.md`',
        '- quantitative index: `results/quantitative_evaluation/QUANTITATIVE_EVALUATION_INDEX.md`',
        "",
        "## Step Results",
        ""
    ) + $stepLines + @(
        "",
        "## Problem 3 Seed Sweep Gate",
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
        "## Safe Claim",
        "",
        $safeClaim,
        "",
        "## Git Status",
        "",
        '```text'
    ) + $gitStatus + @(
        '```'
    )

    if (-not (Test-Path -LiteralPath $submissionSummaryPath)) {
        $lines += @("", "Warning: submission summary was not found.")
    }
    if (-not (Test-Path -LiteralPath $quantIndexPath) -and -not $SkipQuantitativeEvaluation) {
        $lines += @("", "Warning: quantitative evaluation index was not found.")
    }

    $lines -join "`n" | Set-Content -LiteralPath $resolvedPath -Encoding UTF8
    Write-Step "Wrote final status: $resolvedPath"
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$projectPython = Resolve-ProjectPython -RequestedPython $Python
$script:StepResults = @()
$consoleState = $null

Push-Location $repoRoot
try {
    $consoleState = Disable-QuickEditMode
    Initialize-KeepAwake -DisplayOff:$KeepDisplayOff

    Write-Step "Final competition automation started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Python: $projectPython"

    $currentBranch = (git branch --show-current).Trim()
    if ($currentBranch -ne "main" -and -not $AllowNonMainBranch) {
        throw "Current branch is '$currentBranch'. Switch to main or pass -AllowNonMainBranch intentionally."
    }

    if (-not $SkipTeamSync) {
        Invoke-AutomationStep -Name "team sync" -Action {
            & (Join-Path $PSScriptRoot "sync_latest_team_changes.ps1")
            Assert-LastExitCode "sync_latest_team_changes.ps1"
        }
    }
    else {
        Add-StepResult -Name "team sync" -Status "skipped"
    }

    if (-not $SkipQuantitativeEvaluation) {
        Invoke-AutomationStep -Name "quantitative evaluation" -Action {
            & $projectPython scripts/run_quantitative_evaluation.py
            Assert-LastExitCode "run_quantitative_evaluation.py"
        }
    }
    else {
        Add-StepResult -Name "quantitative evaluation" -Status "skipped"
    }

    if (-not $SkipFinalPipeline) {
        Invoke-AutomationStep -Name "final pipeline" -Action {
            & (Join-Path $PSScriptRoot "run_final_pipeline_visible.ps1") `
                -Seeds $Seeds `
                -Python $projectPython `
                -SkipTeamSync
            Assert-LastExitCode "run_final_pipeline_visible.ps1"
        }
    }
    else {
        Add-StepResult -Name "final pipeline" -Status "skipped"
    }

    if (-not $SkipIssueSync) {
        Invoke-AutomationStep -Name "github issue sync" -Action {
            & (Join-Path $PSScriptRoot "sync_hackathon_issues.ps1") -Apply
            Assert-LastExitCode "sync_hackathon_issues.ps1 -Apply"
        }
    }
    else {
        Add-StepResult -Name "github issue sync" -Status "skipped"
    }

    Write-FinalStatus -Path $StatusOutput
    Write-Step "Final competition automation finished."
}
finally {
    Clear-KeepAwake
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
}
