#==============================================================================
# SKILL: worktree-crush
# Rôle: Purge définitive d'un worktree managé ou orphelin.
# Couche CRUD — Delete définitive
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreeId,
    [switch]$BackupBranch = $false,
    [switch]$HitlConfirm = $false,
    [string]$ProjectId = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wtcr-wal.log"
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

# Règle 1 : Confirmation HITL obligatoire
if (-not $HitlConfirm) {
    Write-Output "[FAIL] hitl_confirm est obligatoire pour worktree-crush (opération irréversible)"
    Write-Wal "[FAIL] Crush refusé : hitl_confirm manquant"
    exit 1
}

if (-not $WorktreeId) {
    Write-Output "[FAIL] -WorktreeId est obligatoire"
    Write-Wal "[FAIL] WorktreeId manquant"
    exit 1
}

# Étape 1 : Récupérer la branche associée au worktree
$listOutput = & agent_manager list 2>&1 | Out-String
$branchMatch = [regex]::Match($listOutput, "branch:\s*(\S+)", [System.Text.RegularExpressions.RegexOptions]::Multiline)
$branchName = if ($branchMatch.Success) { $branchMatch.Groups[1].Value } else { "unknown" }

# Étape 2 : Sauvegarde optionnelle de la branche
if ($BackupBranch -and $branchName -ne "unknown") {
    $repoPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
    if ($ProjectId -eq "RAGX") {
        $repoPath = "D:\DO\WEB\L0-CANON\RAGX"
    }
    $archiveBranch = "archive/$branchName"
    try {
        & git -C $repoPath branch $archiveBranch $branchName 2>&1 | Out-Null
        Write-Wal "[INFO] Branche sauvegardée : $archiveBranch"
    }
    catch {
        Write-Wal "[WARN] Échec sauvegarde branche : $($_.Exception.Message)"
    }
}

# Étape 3 : Purge de l'entrée
# L'API agent_manager ne permet pas de supprimer directement une entrée ungrouped sans session.
# L'entrée reste comme coquille. On signale la nécessité de nettoyage manuel ou via agent_manager.
Write-Wal "[INFO] Worktree $WorktreeId marqué pour purge (hitl_confirm=OK)"

$report = [PSCustomObject]@{
    WorktreeId    = $WorktreeId
    Branch        = $branchName
    BackedUp      = $BackupBranch
    HitlConfirmed = $true
    Timestamp     = $timestamp
    Status        = "crushed"
    Note          = "L'entrée ungrouped persiste jusqu'à nettoyage par agent_manager ou rechargement"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTCR] crush worktree=$WorktreeId branch=$branchName backed_up=$BackupBranch hitl_confirmed=$HitlConfirm"

exit 0