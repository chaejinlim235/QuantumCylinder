param(
    [string]$Repository = "chaejinlim235/QuantumCylinder",
    [string]$PlanPath = "",
    [string]$Token = "",
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Get-RepositoryRoot {
    return (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}

function Get-GitHubHeaders {
    param([string]$RequestedToken)

    if ($RequestedToken) {
        return @{
            Authorization = "Bearer $RequestedToken"
            Accept = "application/vnd.github+json"
            "X-GitHub-Api-Version" = "2022-11-28"
            "User-Agent" = "quantum-cylinder-issue-sync"
        }
    }

    if ($env:GITHUB_TOKEN) {
        return @{
            Authorization = "Bearer $env:GITHUB_TOKEN"
            Accept = "application/vnd.github+json"
            "X-GitHub-Api-Version" = "2022-11-28"
            "User-Agent" = "quantum-cylinder-issue-sync"
        }
    }

    $bashCommand = Get-Command bash.exe -ErrorAction SilentlyContinue
    if (-not $bashCommand) {
        throw "Could not find bash.exe. Pass -Token or set GITHUB_TOKEN."
    }
    $credentialLines = & $bashCommand.Source -lc "printf 'protocol=https\nhost=github.com\n\n' | git credential fill"
    $credential = @{}
    foreach ($line in $credentialLines) {
        if ($line -match "^(.*?)=(.*)$") {
            $credential[$matches[1]] = $matches[2]
        }
    }

    if (-not $credential.username -or -not $credential.password) {
        throw "Could not read GitHub credentials. Pass -Token or set GITHUB_TOKEN."
    }

    $pair = "{0}:{1}" -f $credential.username, $credential.password
    $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
    return @{
        Authorization = "Basic $basic"
        Accept = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
        "User-Agent" = "quantum-cylinder-issue-sync"
    }
}

function Invoke-GitHubJson {
    param(
        [string]$Method,
        [string]$Path,
        [object]$Body = $null
    )

    $uri = "https://api.github.com/repos/$Repository$Path"
    if ($null -eq $Body) {
        return Invoke-RestMethod -Method $Method -Uri $uri -Headers $script:Headers
    }

    $json = $Body | ConvertTo-Json -Depth 20
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    return Invoke-RestMethod -Method $Method -Uri $uri -Headers $script:Headers -Body $bytes -ContentType "application/json; charset=utf-8"
}

function Get-IssueBody {
    param([object]$Plan)

    if ($Plan.body) {
        return [string]$Plan.body
    }
    if ($Plan.body_lines) {
        return ($Plan.body_lines -join "`n")
    }
    return ""
}

function Sync-Issue {
    param(
        [int]$Number = 0,
        [string]$Title,
        [string]$Body,
        [string[]]$Assignees,
        [string]$State = "open"
    )

    $payload = @{
        title = $Title
        body = $Body
        assignees = $Assignees
        state = $State
    }
    if ($State -eq "closed") {
        $payload.state_reason = "completed"
    }

    if ($Number -gt 0) {
        Write-Host "Update issue #${Number}: $Title"
        if ($Apply) {
            Invoke-GitHubJson -Method Patch -Path "/issues/$Number" -Body $payload | Out-Null
        }
        return
    }

    $existing = $script:Issues | Where-Object { -not $_.pull_request -and $_.title -eq $Title } | Select-Object -First 1
    if ($existing) {
        Write-Host "Update issue #$($existing.number): $Title"
        if ($Apply) {
            Invoke-GitHubJson -Method Patch -Path "/issues/$($existing.number)" -Body $payload | Out-Null
        }
        return
    }

    Write-Host "Create issue: $Title"
    if ($Apply) {
        Invoke-GitHubJson -Method Post -Path "/issues" -Body $payload | Out-Null
    }
}

$repoRoot = Get-RepositoryRoot
if (-not $PlanPath) {
    $PlanPath = Join-Path $repoRoot "docs\github_issue_plan.json"
}
$resolvedPlanPath = (Resolve-Path -LiteralPath $PlanPath).Path

$script:Headers = Get-GitHubHeaders -RequestedToken $Token
$script:Issues = Invoke-GitHubJson -Method Get -Path "/issues?state=all&per_page=100"
$issuePlans = Get-Content -LiteralPath $resolvedPlanPath -Raw -Encoding UTF8 | ConvertFrom-Json

foreach ($plan in $issuePlans) {
    $assignees = @()
    if ($plan.assignees) {
        $assignees = @($plan.assignees | ForEach-Object { [string]$_ })
    }

    Sync-Issue `
        -Number ([int]$plan.number) `
        -Title ([string]$plan.title) `
        -Body (Get-IssueBody -Plan $plan) `
        -Assignees $assignees `
        -State ([string]$plan.state)
}

if (-not $Apply) {
    Write-Host ""
    Write-Host "Dry run only. Re-run with -Apply to update GitHub issues."
}
