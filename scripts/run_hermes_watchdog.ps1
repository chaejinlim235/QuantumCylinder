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
    Add-SharedUtf8Text -Path $Path -Text ($Message + "`n")
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

function Set-SharedUtf8Text {
    param(
        [string]$Path,
        [string]$Text
    )

    $encoding = [System.Text.UTF8Encoding]::new($false)
    for ($attempt = 1; $attempt -le 20; $attempt++) {
        try {
            $stream = [System.IO.File]::Open(
                $Path,
                [System.IO.FileMode]::Create,
                [System.IO.FileAccess]::Write,
                [System.IO.FileShare]::ReadWrite
            )
            try {
                $writer = [System.IO.StreamWriter]::new($stream, $encoding)
                $stream = $null
                try {
                    $writer.Write($Text)
                }
                finally {
                    $writer.Dispose()
                }
            }
            finally {
                if ($stream) {
                    $stream.Dispose()
                }
            }
            return
        }
        catch {
            if ($attempt -eq 20) {
                throw
            }
            Start-Sleep -Milliseconds 250
        }
    }
}

function Add-SharedUtf8Text {
    param(
        [string]$Path,
        [string]$Text
    )

    $encoding = [System.Text.UTF8Encoding]::new($false)
    for ($attempt = 1; $attempt -le 20; $attempt++) {
        try {
            $stream = [System.IO.File]::Open(
                $Path,
                [System.IO.FileMode]::Append,
                [System.IO.FileAccess]::Write,
                [System.IO.FileShare]::ReadWrite
            )
            try {
                $writer = [System.IO.StreamWriter]::new($stream, $encoding)
                $stream = $null
                try {
                    $writer.Write($Text)
                }
                finally {
                    $writer.Dispose()
                }
            }
            finally {
                if ($stream) {
                    $stream.Dispose()
                }
            }
            return
        }
        catch {
            if ($attempt -eq 20) {
                throw
            }
            Start-Sleep -Milliseconds 250
        }
    }
}

function Write-State {
    param(
        [string]$Path,
        [hashtable]$State
    )

    $State["updated_at"] = (Get-Date).ToString("s")
    Set-SharedUtf8Text -Path $Path -Text (($State | ConvertTo-Json -Depth 5) + "`n")
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
Set-SharedUtf8Text -Path $lockPath -Text (($lock | ConvertTo-Json) + "`n")

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

        $invokeArguments = @(
            $Task,
            "-MaxTurns", "$MaxTurns"
        )
        if ($HermesPath) {
            $invokeArguments += @("-HermesPath", $HermesPath)
        }
        if ($Model) {
            $invokeArguments += @("-Model", $Model)
        }
        if ($Yolo) {
            $invokeArguments += "-Yolo"
        }
        if ($Worktree) {
            $invokeArguments += "-Worktree"
        }

        $childOutPath = Join-Path $logRootPath "$runId-$Task-attempt-$attempt.stdout.log"
        $childErrPath = Join-Path $logRootPath "$runId-$Task-attempt-$attempt.stderr.log"
        Set-SharedUtf8Text -Path $childErrPath -Text ""
        $invokeCommand = "& " + (ConvertTo-CommandLineArgument $invokeScript)
        if ($invokeArguments.Count -gt 0) {
            $invokeCommand += " " + (($invokeArguments | ForEach-Object { ConvertTo-CommandLineArgument $_ }) -join " ")
        }
        $innerCommand = "$invokeCommand *> $(ConvertTo-CommandLineArgument $childOutPath); exit `$LASTEXITCODE"
        $wrapperArguments = @(
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command", $innerCommand
        )
        $childCommandLine = ($wrapperArguments | ForEach-Object { ConvertTo-CommandLineArgument $_ }) -join " "
        Add-LogLine -Path $logPath -Message "[$(Get-Date -Format "s")] child command: powershell.exe $childCommandLine"
        Add-LogLine -Path $logPath -Message "[$(Get-Date -Format "s")] child combined output: $childOutPath"
        Add-LogLine -Path $logPath -Message "[$(Get-Date -Format "s")] child stderr placeholder: $childErrPath"

        $process = Start-Process `
            -FilePath (Get-Command powershell.exe).Source `
            -ArgumentList $childCommandLine `
            -WorkingDirectory $repoRoot `
            -WindowStyle Hidden `
            -PassThru

        $lastOutputAt = Get-Date
        $lastOutLength = 0
        $lastTreeCount = 0
        $childPid = $process.Id
        Add-LogLine -Path $logPath -Message ("[{0}] watchdog: child pid: {1}" -f (Get-Date -Format "HH:mm:ss"), $childPid)

        $startedAt = Get-Date
        $killedForIdle = $false

        while (-not $process.HasExited) {
            Start-Sleep -Seconds $HeartbeatSeconds
            $process.Refresh()
            $now = Get-Date
            $elapsed = New-TimeSpan -Start $startedAt -End $now
            $currentOutLength = if (Test-Path -LiteralPath $childOutPath) { (Get-Item -LiteralPath $childOutPath).Length } else { 0 }
            $currentTreeCount = 0
            try {
                $childProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $childPid" -ErrorAction SilentlyContinue
                if ($childProcess) {
                    $childTree = @(Get-CimInstance Win32_Process | Where-Object {
                        $_.ProcessId -eq $childPid -or $_.ParentProcessId -eq $childPid
                    })
                    $currentTreeCount = $childTree.Count
                }
            }
            catch {
                $currentTreeCount = 0
            }
            if ($currentOutLength -ne $lastOutLength -or $currentTreeCount -ne $lastTreeCount) {
                $lastOutputAt = $now
                $changeMessage = "[{0}] watchdog: child stdout bytes={1} process_tree={2}" -f `
                    (Get-Date -Format "HH:mm:ss"), `
                    $currentOutLength, `
                    $currentTreeCount
                Write-Host $changeMessage -ForegroundColor DarkGray
                Add-LogLine -Path $logPath -Message $changeMessage
                $lastOutLength = $currentOutLength
                $lastTreeCount = $currentTreeCount
            }
            $idle = New-TimeSpan -Start $lastOutputAt -End $now
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
        $process.Refresh()
        $exitCode = if ($killedForIdle) { 124 } else { [int]$process.ExitCode }
        $finalExitCode = $exitCode
        Add-LogLine -Path $logPath -Message ("[{0}] watchdog: child combined output log: {1}" -f (Get-Date -Format "HH:mm:ss"), $childOutPath)
        Add-LogLine -Path $logPath -Message ("[{0}] watchdog: child stderr placeholder: {1}" -f (Get-Date -Format "HH:mm:ss"), $childErrPath)

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
