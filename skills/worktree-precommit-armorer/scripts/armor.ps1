#==============================================================================
# SKILL: worktree-precommit-armorer
# Rôle: Armer immédiatement les garde-fous Git du nouveau worktree (core.hooksPath vers .githooks du repo maître).
# Couche Worktree Engineering — Sécurisation
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreePath = $env:WORKTREE_PATH,
    [string]$RepoPath = $env:REPO_PATH
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wpa-wal.log" -Append -Encoding UTF8
}

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    Write-Output "[FAIL] -WorktreePath invalide ou introuvable : $WorktreePath"
    Write-Wal "[FAIL] WorktreePath invalide : $WorktreePath"
    exit 1
}

if (-not $RepoPath -or -not (Test-Path -LiteralPath $RepoPath)) {
    Write-Output "[FAIL] -RepoPath invalide ou introuvable : $RepoPath"
    Write-Wal "[FAIL] RepoPath invalide : $RepoPath"
    exit 1
}

# Le dossier .githooks du repo maître
$masterHooks = Join-Path $RepoPath ".githooks"
if (-not (Test-Path -LiteralPath $masterHooks)) {
    Write-Output "[WARN] .githooks introuvable dans le repo maître : $masterHooks"
    Write-Wal "[WARN] .githooks introuvable : $masterHooks"
}

# Configurer core.hooksPath dans le worktree
try {
    & git -C $WorktreePath config core.hooksPath $masterHooks 2>&1 | Out-Null
    $hooksConfigured = $true
    Write-Wal "[WPA] core.hooksPath configuré : $masterHooks"
}
catch {
    $hooksConfigured = $false
    Write-Wal "[FAIL] Échec configuration hooks : $($_.Exception.Message)"
}

# Vérifier que la configuration a été prise en compte
$verify = & git -C $WorktreePath config --get core.hooksPath 2>&1 | Out-String | Trim()
$hooksVerified = ($verify -eq $masterHooks)

$report = [PSCustomObject]@{
    Timestamp       = $timestamp
    WorktreePath    = $WorktreePath
    RepoPath        = $RepoPath
    MasterHooks     = $masterHooks
    HooksConfigured = $hooksConfigured
    HooksVerified   = $hooksVerified
    CurrentValue    = $verify
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WPA] armor worktree=$WorktreePath hooks=$masterHooks configured=$hooksConfigured verified=$hooksVerified"

if (-not $hooksVerified) {
    exit 1
}
exit 0