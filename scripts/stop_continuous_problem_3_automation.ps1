param(
    [string]$LogRoot = "logs/continuous_problem_3"
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

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$logRootPath = if ([System.IO.Path]::IsPathRooted($LogRoot)) {
    $LogRoot
}
else {
    Join-Path $repoRoot $LogRoot
}

$lockPath = Join-Path $logRootPath "watchdog.lock.json"
if (-not (Test-Path -LiteralPath $lockPath)) {
    Write-Step "No continuous Problem 3 watchdog lock found."
    return
}

$lock = Get-Content -LiteralPath $lockPath -Raw -Encoding UTF8 | ConvertFrom-Json
$rootPid = [int]$lock.pid
$processes = @(Get-CimInstance Win32_Process)
$targetIds = @()

if (Get-Process -Id $rootPid -ErrorAction SilentlyContinue) {
    $targetIds += $rootPid
}
$targetIds += Get-ChildProcessIds -ParentProcessId $rootPid -Processes $processes
$targetIds = @($targetIds | Select-Object -Unique | Sort-Object -Descending)

if ($targetIds.Count -eq 0) {
    Write-Step "No live process tree found for stale watchdog PID $rootPid."
}
else {
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

Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
Write-Step "Removed lock: $lockPath"
