#==============================================================================
# SKILL: worktree-mission-checker
# Rôle: Valider la présence et l'intégrité du contrat de mission WORKTREE_MISSION.md
# d'un worktree en lecture seule (Read-Only).
# Couche Worktree Engineering — Diagnostic
#==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$WorktreePath,
    [Parameter(Mandatory)] [string]$BranchName,
    [Parameter(Mandatory)] [string]$SessionId
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wmc-wal.log" -Append -Encoding UTF8
}

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    Write-Output "[FAIL] -WorktreePath invalide ou introuvable : $WorktreePath"
    Write-Wal "[FAIL] WorktreePath invalide : $WorktreePath"
    exit 1
}

$missionPath = Join-Path $WorktreePath "WORKTREE_MISSION.md"
$critical = $false

if (-not (Test-Path -LiteralPath $missionPath)) {
    $report = [PSCustomObject]@{
        Timestamp    = $timestamp
        WorktreePath = $WorktreePath
        BranchName   = $BranchName
        SessionId    = $SessionId
        MissionFound = $false
        Status       = "MISSING"
        Detail       = "WORKTREE_MISSION.md absent à la racine du worktree"
    }
    $critical = $true
}
else {
    try {
        $content = Get-Content -LiteralPath $missionPath -Raw -Encoding UTF8
        $hasSession = $content -match "Session ID.*$SessionId"
        $hasBranch  = $content -match "Branch.*$BranchName"
        $hasIntent  = $content -match "Intent Hash"
        $hasTs      = $content -match "Horodatage|Timestamp"

        $report = [PSCustomObject]@{
            Timestamp    = $timestamp
            WorktreePath = $WorktreePath
            BranchName   = $BranchName
            SessionId    = $SessionId
            MissionFound = $true
            Status       = if ($hasSession -and $hasBranch -and $hasIntent -and $hasTs) { "OK" } else { "INCOMPLETE" }
            SessionMatch = $hasSession
            BranchMatch  = $hasBranch
            IntentHash   = $hasIntent
            HasTimestamp = $hasTs
            Detail       = if ($hasSession -and $hasBranch -and $hasIntent -and $hasTs) { "Contrat complet et cohérent" } else { "Contrat présent mais champs manquants" }
        }
        if (-not ($hasSession -and $hasBranch -and $hasIntent -and $hasTs)) {
            $critical = $true
        }
    }
    catch {
        $report = [PSCustomObject]@{
            Timestamp    = $timestamp
            WorktreePath = $WorktreePath
            BranchName   = $BranchName
            SessionId    = $SessionId
            MissionFound = $true
            Status       = "ERROR"
            Detail       = "Erreur de lecture : $($_.Exception.Message)"
        }
        $critical = $true
    }
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WMC] vérification mission worktree=$WorktreePath statut=$($report.Status) critique=$critical"

if ($critical) {
    exit 1
}
exit 0
