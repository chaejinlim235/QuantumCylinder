param(
    [string]$LogRoot = "logs/problem_3_finalist_autopilot"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Get-ChildProcessIds {
    param(
        [int]$ParentProcessId,
        [object[]]$Processes
    )

    $children = @($Processes | Where-Object { $_.ParentProcessId -eq $ParentProcessId })
    $ids = @()
    foreach ($child in $children) {
        $ids += [int]$child.ProcessId
        $ids += Get-ChildProcessIds -ParentProcessId ([int]$child.ProcessId) -Processes $Processes
    }
    return $ids
}

function Stop-ProcessTree {
    param([int]$RootPid)

    $processes = @(Get-CimInstance Win32_Process)
    $targetIds = @()
    if (Get-Process -Id $RootPid -ErrorAction SilentlyContinue) {
        $targetIds += $RootPid
    }
    $targetIds += Get-ChildProcessIds -ParentProcessId $RootPid -Processes $processes
    $targetIds = @($targetIds | Select-Object -Unique | Sort-Object -Descending)

    if ($targetIds.Count -eq 0) {
        Write-Step "No live process tree found for PID $RootPid."
        return
    }

    foreach ($targetPid in $targetIds) {
        try {
            Stop-Process -Id $targetPid -Force -ErrorAction Stop
            Write-Step "Stopped process PID $targetPid."
        }
        catch {
            Write-Step "Could not stop PID ${targetPid}: $($_.Exception.Message)"
        }
    }
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$logRootPath = if ([System.IO.Path]::IsPathRooted($LogRoot)) {
    $LogRoot
}
else {
    Join-Path $repoRoot $LogRoot
}

$stoppedSomething = $false

$watchdogLockPath = Join-Path $logRootPath "watchdog.lock.json"
if (Test-Path -LiteralPath $watchdogLockPath) {
    $lock = Get-Content -LiteralPath $watchdogLockPath -Raw -Encoding UTF8 | ConvertFrom-Json
    Stop-ProcessTree -RootPid ([int]$lock.pid)
    Remove-Item -LiteralPath $watchdogLockPath -Force -ErrorAction SilentlyContinue
    Write-Step "Removed watchdog lock: $watchdogLockPath"
    $stoppedSomething = $true
}

$detachedPath = Join-Path $logRootPath "detached_process.json"
if (Test-Path -LiteralPath $detachedPath) {
    $detached = Get-Content -LiteralPath $detachedPath -Raw -Encoding UTF8 | ConvertFrom-Json
    Stop-ProcessTree -RootPid ([int]$detached.pid)
    Remove-Item -LiteralPath $detachedPath -Force -ErrorAction SilentlyContinue
    Write-Step "Removed detached process file: $detachedPath"
    $stoppedSomething = $true
}

if (-not $stoppedSomething) {
    Write-Step "No Problem 3 finalist autopilot lock or detached process file found."
}
