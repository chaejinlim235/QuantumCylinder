param(
    [string]$Remote = "origin",
    [string]$Branch = "main",
    [switch]$NoMerge
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Get-StatusPaths {
    $paths = @()
    $lines = @(git status --porcelain)
    foreach ($line in $lines) {
        if (-not $line) {
            continue
        }
        $path = $line.Substring(3)
        if ($path -match " -> ") {
            $path = ($path -split " -> ")[-1]
        }
        $paths += $path.Trim('"')
    }
    return $paths
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path

Push-Location $repoRoot
try {
    Write-Step "Syncing latest team changes."
    Write-Step "Repository: $repoRoot"

    $currentBranch = (git branch --show-current).Trim()
    Write-Step "Current branch: $currentBranch"

    Write-Step "Fetching $Remote."
    git fetch --prune $Remote

    $targetRef = "$Remote/$Branch"
    $targetExists = $true
    git rev-parse --verify $targetRef | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $targetExists = $false
    }
    if (-not $targetExists) {
        throw "Remote target does not exist: $targetRef"
    }

    $dirtyPaths = @(Get-StatusPaths)
    if ($dirtyPaths.Count -gt 0) {
        Write-Step "Local working tree has existing changes."
        $dirtyPaths | ForEach-Object { Write-Host "  local: $_" }
    }
    else {
        Write-Step "Local working tree has no existing changes."
    }

    if ($currentBranch -ne $Branch) {
        Write-Step "Not on $Branch. Fetch completed, but automatic merge is skipped."
        git status --short --branch
        return
    }

    $incomingPaths = @(git diff --name-only HEAD $targetRef | Where-Object { $_ })
    if ($incomingPaths.Count -eq 0) {
        Write-Step "No incoming file changes from $targetRef."
    }
    else {
        Write-Step "Incoming file changes from $targetRef."
        $incomingPaths | ForEach-Object { Write-Host "  incoming: $_" }
    }

    $overlap = @($dirtyPaths | Where-Object { $incomingPaths -contains $_ })
    if ($overlap.Count -gt 0) {
        Write-Step "Automatic sync stopped because local changes overlap incoming files."
        $overlap | ForEach-Object { Write-Host "  overlap: $_" }
        throw "Resolve or commit/stash overlapping local changes before syncing."
    }

    if ($NoMerge) {
        Write-Step "NoMerge was set. Fetch/status only."
    }
    else {
        Write-Step "Fast-forward merging $targetRef."
        git merge --ff-only $targetRef
    }

    Write-Step "Post-sync git status."
    git status --short --branch

    Write-Step "Recent commits."
    git log --oneline --max-count 5
}
finally {
    Pop-Location
}
