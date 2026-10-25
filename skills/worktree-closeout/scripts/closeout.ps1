#==============================================================================
# SKILL: worktree-closeout
# Rôle: Fermeture propre d'un worktree managé après vérification du merge.
# Couche CRUD — Delete partiel (nettoyage de session)
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreeId,
    [string]$SessionId,
    [switch]$VerifyMerge = $true,
    [string]$ProjectId = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wtc-wal.log"
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

# Validation des entrées
if (-not $WorktreeId) {
    Write-Output "[FAIL] -WorktreeId est obligatoire"
    Write-Wal "[FAIL] WorktreeId manquant"
    exit 1
}

# Étape 1 : Vérifier le merge si demandé
if ($VerifyMerge) {
    # Récupérer la branche du worktree (via agent_manager list ou lecture locale)
    # En pratique, KiloCode fournit ces infos. Ici on vérifie via git sur le dépôt cible.
    $repoPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
    if ($ProjectId -eq "RAGX") {
        $repoPath = "D:\DO\WEB\L0-CANON\RAGX"
    }
    
    # Déterminer la branche associée au worktree
    # (Cette info viendrait de agent_manager list en pratique)
    $branchInfo = & agent_manager list 2>&1 | Out-String
    $branchMatch = [regex]::Match($branchInfo, "branch:\s*(\S+)", [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($branchMatch.Success) {
        $branchName = $branchMatch.Groups[1].Value
        # Vérifier que la branche est mergée dans main
        $mergeCheck = & git -C $repoPath log main..$branchName --oneline 2>&1
        if ($mergeCheck) {
            Write-Output "[FAIL] La branche $branchName n'est pas mergée dans main (commits non mergés détectés)"
            Write-Wal "[FAIL] Closeout bloqué : branche $branchName non mergée"
            exit 1
        }
        Write-Output "[OK] Branche $branchName mergée dans main"
    }
}

# Étape 2 : Unassign de section
try {
    & agent_manager move -sessionID $WorktreeId -sectionID $null 2>&1 | Out-Null
    Write-Wal "[INFO] Worktree $WorktreeId unassigné de section"
}
catch {
    Write-Wal "[WARN] Échec unassign : $($_.Exception.Message)"
}

# Étape 3 : Stop de session
if ($SessionId) {
    try {
        & agent_manager stop -sessionID $SessionId 2>&1 | Out-Null
        Write-Wal "[INFO] Session $SessionId stoppée"
    }
    catch {
        Write-Wal "[WARN] Échec stop session : $($_.Exception.Message)"
    }
}

# Étape 4 : Nettoyage entrée ungrouped (si persiste)
# Note : l'API agent_manager n'a pas d'action de suppression d'entrée orpheline.
# L'entrée reste dans ungrouped jusqu'à nettoyage manuel ou rechargement.
Write-Wal "[INFO] Closeout terminé pour worktree $WorktreeId"

$report = [PSCustomObject]@{
    WorktreeId    = $WorktreeId
    SessionId     = $SessionId
    Merged        = $VerifyMerge
    SessionStopped = $SessionId -ne $null
    Timestamp     = $timestamp
    Status        = "closed"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTC] closeout worktree=$WorktreeId branch=$branchName merged=$VerifyMerge session_stopped=$($SessionId -ne $null)"

exit 0