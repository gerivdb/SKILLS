#==============================================================================
# SKILL: worktree-genetic-contractor
# Rôle: Générer WORKTREE_MISSION.md à la naissance du worktree (contrat de mission, périmètre, dépendances, IntentHash).
# Couche Worktree Engineering — Héritage génétique
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreePath = $env:WORKTREE_PATH,
    [string]$RepoPath = $env:REPO_PATH,
    [string]$BranchName,
    [string]$SessionId,
    [string]$IntentHash
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wgc-wal.log" -Append -Encoding UTF8
}

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    Write-Output "[FAIL] -WorktreePath invalide ou introuvable : $WorktreePath"
    Write-Wal "[FAIL] WorktreePath invalide : $WorktreePath"
    exit 1
}

if (-not $BranchName) {
    # Tenter de récupérer depuis le dépôt
    try {
        $BranchName = & git -C $RepoPath branch --show-current 2>&1 | Out-String | Trim()
    }
    catch {
        $BranchName = "unknown"
    }
}

# Déterminer le périmètre selon le préfixe de branche
$scope = "Général — aucun périmètre spécifique défini"
$allowedFiles = []
$forbiddenFiles = @()

if ($BranchName -like "feat/citizen-*") {
    $scope = "Citizen L3 + Skills L4 — fichiers citoyens et skills autorisés uniquement"
    $allowedFiles = @("citizens/*", "skills/*", "SKILL.md", "REGISTRY.yaml")
    $forbiddenFiles = @("L0-CANON/*", "L1-INFRA/*", ".git/*")
}
elseif ($BranchName -like "feat/gericode-*") {
    $scope = "GeriCode L2 + ACT Protocol — fichiers GeriCode et ACT autorisés uniquement"
    $allowedFiles = @("GeriCode/*", "ACT/*", "beads.json", "ACT-*")
    $forbiddenFiles = @("L0-CANON/*", "L4-TOOLS/*", ".git/*")
}
elseif ($BranchName -like "feat/worktree-*") {
    $scope = "Worktree operator skills L4 — fichiers de skills et scripts uniquement"
    $allowedFiles = @("skills/*", "scripts/*", "SKILL.md", "REGISTRY.yaml")
    $forbiddenFiles = @("L0-CANON/*", "L1-INFRA/*", ".git/*")
}

$missionContent = @"
# WORKTREE_MISSION.md

## Contexte
Ce worktree a été créé automatiquement par le `setup-script.ps1` de Kilo Code.
Il est régi par un contrat de mission strict généré par le skill `worktree-genetic-contractor`.

## Informations de session
- **Worktree path** : $WorktreePath
- **Repo maître** : $RepoPath
- **Branche** : $BranchName
- **Session ID** : $SessionId
- **IntentHash** : $IntentHash
- **Horodatage de création** : $timestamp

## Périmètre strict (fichiers autorisés)
$scope

### Fichiers touchables (autorisés)
$allowedFiles

### Fichiers interdits (ne jamais modifier)
$forbiddenFiles

## Dépendances parentes
Ce worktree dépend du repo maître : $RepoPath
Toute modification doit être compatible avec l'état actuel de `main`.

## Commande de test unitaire
Avant toute clôture de session, exécuter la commande de test unitaire appropriée pour valider que le travail est correct :
- Pour les skills PowerShell : `pwsh -ExecutionPolicy Bypass -File <chemin_du_script>.ps1`
- Pour les skills Python : `python <chemin_du_script>.py`
- Pour les skills Zig : `zig build test` ou `zig test`

## Règles de conduite
1. Ne jamais modifier de fichiers en dehors du périmètre autorisé ci-dessus.
2. Toujours vérifier que `git branch --merged main` inclut cette branche avant clôture.
3. Toujours exécuter le `worktree-lifecycle-reaper` à la fin de la session.
4. Toute violation du périmètre doit être signalée immédiatement.

---

*Généré automatiquement par worktree-genetic-contractor le $timestamp*
"@

$missionPath = Join-Path $WorktreePath "WORKTREE_MISSION.md"
try {
    $missionContent | Out-File -FilePath $missionPath -Encoding UTF8
    Write-Wal "[WGC] contrat généré : $missionPath branche=$BranchName"
}
catch {
    Write-Output "[FAIL] Impossible d'écrire WORKTREE_MISSION.md : $($_.Exception.Message)"
    Write-Wal "[FAIL] Écriture contrat échouée : $($_.Exception.Message)"
    exit 1
}

$report = [PSCustomObject]@{
    Timestamp      = $timestamp
    WorktreePath   = $WorktreePath
    BranchName     = $BranchName
    SessionId      = $SessionId
    IntentHash     = $IntentHash
    Scope          = $scope
    MissionPath    = $missionPath
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WGC] contrat généré : worktree=$WorktreePath branche=$BranchName mission=$missionPath"

exit 0