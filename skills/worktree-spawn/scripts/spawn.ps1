#==============================================================================
# SKILL: worktree-spawn
# Rôle: Créer un nouveau worktree managé dans un projet Agent Manager.
# Couche CRUD — Create
#==============================================================================

[CmdletBinding()]
param(
    [string]$ProjectId,
    [string]$BranchName,
    [string]$BaseBranch = "main",
    [string]$SessionName = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wts-wal.log"
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
if (-not $ProjectId) {
    Write-Output "[FAIL] -ProjectId est obligatoire (RAGX ou SKILLS)"
    Write-Wal "[FAIL] ProjectId manquant"
    exit 1
}
if (-not $BranchName) {
    Write-Output "[FAIL] -BranchName est obligatoire"
    Write-Wal "[FAIL] BranchName manquant"
    exit 1
}

# Déterminer le chemin du dépôt
$repoPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
if ($ProjectId -eq "RAGX") {
    $repoPath = "D:\DO\WEB\L0-CANON\RAGX"
}

# Étape 1 : Vérifier que la branche n'existe pas déjà
$existingBranches = & git -C $repoPath branch --list $BranchName 2>&1
if ($existingBranches) {
    Write-Output "[FAIL] La branche $BranchName existe déjà dans $ProjectId"
    Write-Wal "[FAIL] Branche dupliquée : $BranchName"
    exit 1
}

# Étape 2 : Créer la branche depuis baseBranch
try {
    & git -C $repoPath checkout -b $BranchName $BaseBranch 2>&1 | Out-Null
    Write-Wal "[INFO] Branche créée : $BranchName depuis $BaseBranch"
}
catch {
    Write-Output "[FAIL] Impossible de créer la branche : $($_.Exception.Message)"
    Write-Wal "[FAIL] Création branche échouée : $BranchName"
    exit 1
}

# Étape 3 : Instancier le worktree via Agent Manager
# L'appel agent_manager avec mode: worktree est fait par KiloCode directement.
# Ce skill prépare le terrain et signale la création.
Write-Wal "[INFO] Worktree à créer : project=$ProjectId branch=$BranchName base=$BaseBranch session=$SessionName"

$report = [PSCustomObject]@{
    ProjectId    = $ProjectId
    BranchName   = $BranchName
    BaseBranch   = $BaseBranch
    SessionName  = $SessionName
    Timestamp    = $timestamp
    Status       = "spawn_ready"
    Note         = "Appeler agent_manager avec mode: worktree pour finaliser la création"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTS] spawn project=$ProjectId branch=$BranchName base=$BaseBranch session=$SessionName"

exit 0