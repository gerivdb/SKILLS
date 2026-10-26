#==============================================================================
# SKILL: worktree-synaptic-bus-joiner
# Rôle: Enrôlement du nouveau worktree dans le bus inter-worktrees .kilo/bus/ et émission de session-spawned.json.
# Couche Worktree Engineering — Enregistrement
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreePath = $env:WORKTREE_PATH,
    [string]$WorktreeId,
    [string]$SessionId,
    [string]$BranchName
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wsbj-wal.log" -Append -Encoding UTF8
}

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    Write-Output "[FAIL] -WorktreePath invalide ou introuvable : $WorktreePath"
    Write-Wal "[FAIL] WorktreePath invalide : $WorktreePath"
    exit 1
}

# Créer le dossier .kilo/bus/ dans le worktree
$busDir = Join-Path $WorktreePath ".kilo\bus"
try {
    New-Item -ItemType Directory -Force -Path $busDir | Out-Null
}
catch {
    Write-Output "[FAIL] Impossible de créer .kilo/bus/ : $($_.Exception.Message)"
    Write-Wal "[FAIL] Création bus échouée : $($_.Exception.Message)"
    exit 1
}

# Générer le fichier session-spawned.json
$signal = [PSCustomObject]@{
    WorktreeId     = $WorktreeId
    SessionId      = $SessionId
    BranchName     = $BranchName
    TimestampUtc   = $timestamp
    WorktreePath   = $WorktreePath
    Event          = "session-spawned"
}

$signalPath = Join-Path $busDir "session-spawned.json"
try {
    $signal | ConvertTo-Json -Depth 3 | Out-File -FilePath $signalPath -Encoding UTF8
}
catch {
    Write-Output "[FAIL] Impossible d'écrire session-spawned.json : $($_.Exception.Message)"
    Write-Wal "[FAIL] Écriture signal échouée : $($_.Exception.Message)"
    exit 1
}

$report = [PSCustomObject]@{
    Timestamp        = $timestamp
    WorktreePath     = $WorktreePath
    WorktreeId       = $WorktreeId
    SessionId        = $SessionId
    BranchName       = $BranchName
    BusDir           = $busDir
    SignalPath       = $signalPath
    Event            = "session-spawned"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WSBJ] join worktree=$WorktreePath session=$SessionId branch=$BranchName signal=$signalPath"

exit 0