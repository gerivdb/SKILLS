#==============================================================================
# SKILL: worktree-revive
# Rôle: Ressusciter un worktree managé orphelin via git reflog.
# Couche CRUD — Restore
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreeId,
    [string]$BranchName,
    [string]$ReflogSha,
    [string]$ProjectId = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wtr-wal.log"
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

if (-not $WorktreeId -and -not $BranchName) {
    Write-Output "[FAIL] -WorktreeId ou -BranchName est obligatoire"
    Write-Wal "[FAIL] Aucun identificateur fourni"
    exit 1
}

$repoPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
if ($ProjectId -eq "RAGX") {
    $repoPath = "D:\DO\WEB\L0-CANON\RAGX"
}

# Étape 1 : Récupérer le SHA via reflog
$sha = $ReflogSha
if (-not $sha) {
    # Chercher dans le reflog les commits de la branche
    $reflogOutput = & git -C $repoPath reflog --format="%H %gs" 2>&1 | Out-String
    if ($BranchName) {
        $branchMatch = [regex]::Match($reflogOutput, "([0-9a-f]{40}).*branch.*$BranchName.*created", [System.Text.RegularExpressions.RegexOptions]::Multiline)
        if ($branchMatch.Success) {
            $sha = $branchMatch.Groups[1].Value
        }
    }
    if (-not $sha) {
        # Prendre le premier commit du reflog comme fallback
        $firstLine = ($reflogOutput -split "`n")[0]
        if ($firstLine -match "^([0-9a-f]{40})") {
            $sha = $matches[1]
        }
    }
}

if (-not $sha) {
    Write-Output "[FAIL] Impossible de trouver un SHA dans le reflog"
    Write-Wal "[FAIL] Reflog vide ou SHA introuvable"
    exit 1
}

Write-Wal "[INFO] SHA retrouvé : $sha"

# Étape 2 : Recréer le worktree
# L'appel git worktree add est fait via KiloCode / agent_manager
Write-Wal "[INFO] Worktree à recréer : sha=$sha branch=$BranchName worktree=$WorktreeId"

$report = [PSCustomObject]@{
    WorktreeId   = $WorktreeId
    BranchName   = $BranchName
    Sha          = $sha
    Timestamp    = $timestamp
    Status       = "revive_ready"
    Note         = "Appeler git worktree add puis agent_manager pour réintégrer"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTR] revive worktree=$WorktreeId branch=$BranchName sha=$sha"

exit 0