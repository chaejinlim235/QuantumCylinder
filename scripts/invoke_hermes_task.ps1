param(
    [Parameter(Position = 0)]
    [ValidateSet("feedback-loop", "final-pipeline", "final-sync-fix", "p3-seed-sweep", "p3-report-draft", "p3-judge-review", "p3-status")]
    [string]$Task = "p3-seed-sweep",

    [string]$HermesPath = "",
    [string]$Model = "",
    [int]$MaxTurns = 120,
    [switch]$Yolo,
    [switch]$Worktree
)

$ErrorActionPreference = "Stop"

function Resolve-HermesPath {
    param([string]$RequestedPath)

    if ($RequestedPath) {
        if (Test-Path -LiteralPath $RequestedPath) {
            return (Resolve-Path -LiteralPath $RequestedPath).Path
        }
        throw "HermesPath does not exist: $RequestedPath"
    }

    $command = Get-Command hermes -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $knownPath = Join-Path $env:LOCALAPPDATA "Hermes\hermes-agent\venv\Scripts\hermes.exe"
    if (Test-Path -LiteralPath $knownPath) {
        return $knownPath
    }

    throw "Could not find hermes. Pass -HermesPath or add Hermes to PATH."
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$taskPath = Join-Path $repoRoot ".hermes\tasks\$Task.md"
if (-not (Test-Path -LiteralPath $taskPath)) {
    throw "Task prompt not found: $taskPath"
}

$hermes = Resolve-HermesPath -RequestedPath $HermesPath
$prompt = Get-Content -LiteralPath $taskPath -Raw -Encoding UTF8
$promptArgument = $prompt.Replace('"', '\"')
$projectPython = Get-Command python -ErrorAction SilentlyContinue
$previousProjectPython = $env:HERMES_PROJECT_PYTHON
$previousProjectRoot = $env:HERMES_PROJECT_ROOT
$previousPath = $env:Path

if ($projectPython) {
    $env:HERMES_PROJECT_PYTHON = $projectPython.Source
    $env:Path = "$(Split-Path -Parent $projectPython.Source);$env:Path"
}
$env:HERMES_PROJECT_ROOT = $repoRoot

$arguments = @("chat", "-q", $promptArgument, "--max-turns", "$MaxTurns", "--accept-hooks")
if ($Yolo) {
    $arguments += "--yolo"
}
if ($Worktree) {
    $arguments += "--worktree"
}
if ($Model) {
    $arguments += @("-m", $Model)
}

Push-Location $repoRoot
try {
    & $hermes @arguments
}
finally {
    Pop-Location
    $env:HERMES_PROJECT_PYTHON = $previousProjectPython
    $env:HERMES_PROJECT_ROOT = $previousProjectRoot
    $env:Path = $previousPath
}
