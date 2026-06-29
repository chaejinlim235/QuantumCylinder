param(
    [Parameter(Position = 0)]
    [ValidateSet("continuous-p3-improvement", "feedback-loop", "final-pipeline", "final-sync-fix", "p3-defense-evidence", "problem-3-finalist-autopilot", "p3-seed-sweep", "p3-report-draft", "p3-judge-review", "p3-status", "quantitative-evaluation")]
    [string]$Task = "final-sync-fix",

    [string]$HermesPath = "",
    [string]$Model = "",
    [int]$MaxTurns = 360,
    [int]$Attempts = 6,
    [int]$RetryDelaySeconds = 60,
    [int]$HeartbeatSeconds = 60,
    [int]$IdleTimeoutMinutes = 45,
    [string]$LogRoot = "logs/hermes_automation",
    [switch]$Yolo,
    [switch]$Worktree,
    [switch]$NoKeepAwake,
    [switch]$KeepDisplayOff,
    [switch]$AllowParallel
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Add-LogLine {
    param(
        [string]$Path,
        [string]$Message
    )
    Add-Content -LiteralPath $Path -Value $Message -Encoding UTF8
}

function Format-RunDuration {
    param([TimeSpan]$Duration)
    return ("{0:00}:{1:00}:{2:00}" -f [int]$Duration.TotalHours, $Duration.Minutes, $Duration.Seconds)
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

function ConvertTo-CommandLineArgument {
    param([string]$Argument)

    if ($Argument -notmatch '[\s"]') {
        return $Argument
    }

    return '"' + ($Argument -replace '"', '\"') + '"'
}

function Write-State {
    param(
        [string]$Path,
        [hashtable]$State
    )

    $State["updated_at"] = (Get-Date).ToString("s")
    $State | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Stop-ProcessTree {
    param([int]$ProcessId)

    taskkill.exe /PID $ProcessId /T /F | Out-Null
}

$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$invokeScript = Join-Path $PSScriptRoot "invoke_hermes_task.ps1"
if (-not (Test-Path -LiteralPath $invokeScript)) {
    throw "Missing invoke script: $invokeScript"
}

if ([System.IO.Path]::IsPathRooted($LogRoot)) {
    $logRootPath = $LogRoot
}
else {
    $logRootPath = Join-Path $repoRoot $LogRoot
}
New-Item -ItemType Directory -Force -Path $logRootPath | Out-Null

$lockPath = Join-Path $logRootPath "watchdog.lock.json"
$statePath = Join-Path $logRootPath "latest_state.json"

if ((Test-Path -LiteralPath $lockPath) -and (-not $AllowParallel)) {
    try {
        $existingLock = Get-Content -LiteralPath $lockPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $existingProcess = Get-Process -Id $existingLock.pid -ErrorAction SilentlyContinue
        if ($existingProcess) {
            throw "Another Hermes watchdog is already running with PID $($existingLock.pid). Use -AllowParallel only if this is intentional."
        }
    }
    catch {
        if ($_.Exception.Message -like "Another Hermes watchdog*") {
            throw
        }
    }
}

$lock = @{
    pid = $PID
    task = $Task
    started_at = (Get-Date).ToString("s")
}
$lock | ConvertTo-Json | Set-Content -LiteralPath $lockPath -Encoding UTF8

$consoleState = $null
$completed = $false
$finalExitCode = 1

Push-Location $repoRoot
try {
    $consoleState = Disable-QuickEditMode

    if (-not $NoKeepAwake) {
        Initialize-KeepAwake -DisplayOff:$KeepDisplayOff
        if ($KeepDisplayOff) {
            Write-Step "Sleep prevention enabled. Display may turn off."
        }
        else {
            Write-Step "Sleep and display-off prevention enabled for this watchdog run."
        }
    }

    Write-Step "Hermes watchdog started."
    Write-Step "Repository: $repoRoot"
    Write-Step "Task: $Task"
    Write-Step "Attempts: $Attempts"
    Write-Step "Idle timeout: $IdleTimeoutMinutes minutes"
    Write-Step "Logs: $logRootPath"

    for ($attempt = 1; $attempt -le $Attempts; $attempt++) {
        $runId = Get-Date -Format "yyyyMMdd_HHmmss"
        $logPath = Join-Path $logRootPath "$runId-$Task-attempt-$attempt.log"

        $state = @{
            status = "running"
            task = $Task
            attempt = $attempt
            attempts = $Attempts
            log = $logPath
            exit_code = $null
        }
        Write-State -Path $statePath -State $state

        Write-Step "Attempt $attempt/$Attempts started."
        Add-LogLine -Path $logPath -Message "[$(Get-Date -Format "s")] Hermes watchdog attempt $attempt/$Attempts"

        $childArguments = @(
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-File", $invokeScript,
            $Task,
            "-MaxTurns", "$MaxTurns"
        )
        if ($HermesPath) {
            $childArguments += @("-HermesPath", $HermesPath)
        }
        if ($Model) {
            $childArguments += @("-Model", $Model)
        }
        if ($Yolo) {
            $childArguments += "-Yolo"
        }
        if ($Worktree) {
            $childArguments += "-Worktree"
        }

        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = (Get-Command powershell.exe).Source
        $psi.Arguments = ($childArguments | ForEach-Object { ConvertTo-CommandLineArgument $_ }) -join " "
        $psi.WorkingDirectory = $repoRoot
        $psi.UseShellExecute = $false
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true

        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $psi
        $script:lastOutputAt = Get-Date
        $script:currentLogPath = $logPath

        $stdoutHandler = [System.Diagnostics.DataReceivedEventHandler]{
            param($sender, $eventArgs)
            if ($null -ne $eventArgs.Data) {
                $script:lastOutputAt = Get-Date
                $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $eventArgs.Data
                Write-Host $line
                Add-Content -LiteralPath $script:currentLogPath -Value $line -Encoding UTF8
            }
        }
        $stderrHandler = [System.Diagnostics.DataReceivedEventHandler]{
            param($sender, $eventArgs)
            if ($null -ne $eventArgs.Data) {
                $script:lastOutputAt = Get-Date
                $line = "[{0}] STDERR: {1}" -f (Get-Date -Format "HH:mm:ss"), $eventArgs.Data
                Write-Host $line -ForegroundColor Yellow
                Add-Content -LiteralPath $script:currentLogPath -Value $line -Encoding UTF8
            }
        }

        $process.add_OutputDataReceived($stdoutHandler)
        $process.add_ErrorDataReceived($stderrHandler)
        [void]$process.Start()
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()

        $startedAt = Get-Date
        $killedForIdle = $false

        while (-not $process.HasExited) {
            Start-Sleep -Seconds $HeartbeatSeconds
            $now = Get-Date
            $elapsed = New-TimeSpan -Start $startedAt -End $now
            $idle = New-TimeSpan -Start $script:lastOutputAt -End $now
            $heartbeat = "[{0}] watchdog: attempt={1}/{2} elapsed={3} idle={4}" -f `
                (Get-Date -Format "HH:mm:ss"), `
                $attempt, `
                $Attempts, `
                (Format-RunDuration -Duration $elapsed), `
                (Format-RunDuration -Duration $idle)
            Write-Host $heartbeat -ForegroundColor DarkGray
            Add-LogLine -Path $logPath -Message $heartbeat

            if ($IdleTimeoutMinutes -gt 0 -and $idle.TotalMinutes -ge $IdleTimeoutMinutes) {
                $message = "[{0}] watchdog: no output for {1} minutes; restarting child process." -f (Get-Date -Format "HH:mm:ss"), $IdleTimeoutMinutes
                Write-Host $message -ForegroundColor Yellow
                Add-LogLine -Path $logPath -Message $message
                Stop-ProcessTree -ProcessId $process.Id
                $killedForIdle = $true
                break
            }
        }

        $process.WaitForExit()
        $exitCode = if ($killedForIdle) { 124 } else { $process.ExitCode }
        $finalExitCode = $exitCode

        $state["status"] = if ($exitCode -eq 0) { "completed" } else { "failed" }
        $state["exit_code"] = $exitCode
        Write-State -Path $statePath -State $state

        Write-Step "Attempt $attempt/$Attempts finished with exit code $exitCode."

        if ($exitCode -eq 0) {
            $completed = $true
            break
        }

        if ($attempt -lt $Attempts) {
            Write-Step "Retrying in $RetryDelaySeconds seconds."
            Start-Sleep -Seconds $RetryDelaySeconds
        }
    }
}
finally {
    if (-not $NoKeepAwake) {
        Clear-KeepAwake
    }
    Restore-ConsoleMode -ConsoleState $consoleState
    Pop-Location
    Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
}

if ($completed) {
    Write-Step "Hermes watchdog completed successfully."
    $global:LASTEXITCODE = 0
    return
}

$global:LASTEXITCODE = $finalExitCode
throw "Hermes watchdog failed after $Attempts attempts. See logs: $logRootPath"
