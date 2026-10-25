#==============================================================================
# SKILL: worktree-sync-all
# Rôle: Fetch explicite + rebase sur main pour tous les worktrees d'un projet.
# Couche CRUD — Update globale
#==============================================================================

[CmdletBinding()]
param(
    [string]$ProjectId,
    [string]$BaseBranch = "main",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wtsa-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

if (-not $ProjectId) {
    Write-Output "[FAIL] -ProjectId est obligatoire (RAGX ou SKILLS)"
    Write-Wal "[FAIL] ProjectId manquant"
    exit 1
}

$repoPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
if ($ProjectId -eq "RAGX") {
    $repoPath = "D:\DO\WEB\L0-CANON\RAGX"
}

# Étape 1 : Fetch explicite (protocole BDCP)
try {
    & git -C $repoPath fetch origin 2>&1 | Out-Null
    Write-Wal "[INFO] Fetch explicite effectué sur $ProjectId"
}
catch {
    Write-Output "[FAIL] Échec du fetch : $($_.Exception.Message)"
    Write-Wal "[FAIL] Fetch échoué : $ProjectId"
    exit 1
}

# Étape 2 : Lister les worktrees et les synchroniser un par un
$listOutput = & agent_manager list 2>&1 | Out-String
# Parsing simplifié — en pratique KiloCode fournit le JSON structuré
$worktrees = @()
$lines = $listOutput -split "`n"
$currentWt = $null
foreach ($line in $lines) {
    if ($line -match "id:\s*(wt-\S+)") {
        if ($currentWt) { $worktrees += $currentWt }
        $currentWt = [PSCustomObject]@{
            Id    = $matches[1]
            State = ""
        }
    }
    elseif ($currentWt -and $line -match "activity:\s*(\w+)") {
        $currentWt.State = $matches[1].Trim()
    }
}
if ($currentWt) { $worktrees += $currentWt }

$synced = 0
$conflicts = 0
$skipped = 0

foreach ($wt in $worktrees) {
    # Ne pas synchroniser les worktrees occupés
    if ($wt.State -eq "busy" -or $wt.State -eq "retry") {
        $skipped++
        Write-Wal "[WARN] Worktree $($wt.Id) ignoré (état : $($wt.State))"
        continue
    }
    
    # Rebase sur baseBranch
    try {
        & git -C $repoPath rebase origin/$BaseBranch 2>&1 | Out-Null
        $synced++
        Write-Wal "[INFO] Worktree $($wt.Id) rebase OK sur $BaseBranch"
    }
    catch {
        $conflicts++
        Write-Wal "[FAIL] Worktree $($wt.Id) conflit lors du rebase"
    }
}

$report = [PSCustomObject]@{
    ProjectId   = $ProjectId
    BaseBranch  = $BaseBranch
    Synced      = $synced
    Conflicts   = $conflicts
    Skipped     = $skipped
    Timestamp   = $timestamp
    Status      = if ($conflicts -eq 0) { "OK" } else { "PARTIAL" }
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTSA] sync_all project=$ProjectId synced=$synced conflicts=$conflicts skipped=$skipped"

if ($conflicts -gt 0) {
    exit 1
}
exit 0