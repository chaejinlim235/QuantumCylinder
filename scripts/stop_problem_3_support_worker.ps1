param(
    [string]$WorkerName = "support",
    [string]$LogRoot = ""
)

$ErrorActionPreference = "Stop"

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
$safeWorkerName = Get-SafeName -Name $WorkerName
if (-not $LogRoot) {
    $LogRoot = "logs/problem_3_support_worker/$safeWorkerName"
}
$logRootPath = if ([System.IO.Path]::IsPathRooted($LogRoot)) {
    $LogRoot
}
else {
    Join-Path $repoRoot $LogRoot
}

$detachedPath = Join-Path $logRootPath "detached_process.json"
if (-not (Test-Path -LiteralPath $detachedPath)) {
    Write-Step "No detached Problem 3 support worker process file found for worker '$WorkerName'."
    return
}

$detached = Get-Content -LiteralPath $detachedPath -Raw -Encoding UTF8 | ConvertFrom-Json
Stop-ProcessTree -RootPid ([int]$detached.pid)
Remove-Item -LiteralPath $detachedPath -Force -ErrorAction SilentlyContinue
Write-Step "Removed detached process file: $detachedPath"
