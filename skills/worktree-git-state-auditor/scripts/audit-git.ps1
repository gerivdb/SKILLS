#==============================================================================
# SKILL: worktree-git-state-auditor
# Rôle: Auditer l'état Git d'un worktree (branche actuelle, fusion dans main)
# en lecture seule (Read-Only).
# Couche Worktree Engineering — Diagnostic
#==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$WorktreePath,
    [Parameter(Mandatory)] [string]$RepoPath,
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
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wgsa-wal.log" -Append -Encoding UTF8
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

$critical = $false

# 1. Branche actuelle du worktree
$currentBranch = "unknown"
try {
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $currentBranch = & git -C $WorktreePath branch --show-current 2>&1 | Out-String | ForEach-Object { $_.Trim() }
    $ErrorActionPreference = $prevEAP
    if (-not $currentBranch) { $currentBranch = "unknown" }
}
catch {
    $currentBranch = "ERROR"
    $critical = $true
}

# 2. Vérification si la branche est mergée dans main du repo maître
$mergedInMain = $false
$mergeDetail = "Non vérifié"
try {
    if ($RepoPath -and (Test-Path -LiteralPath $RepoPath)) {
        $prevEAP = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $merged = & git -C $RepoPath branch --merged main 2>&1 | Out-String
        $ErrorActionPreference = $prevEAP
        if ($merged -match $BranchName) {
            $mergedInMain = $true
            $mergeDetail = "Branche $BranchName mergée dans main"
        }
        else {
            $mergeDetail = "Branche $BranchName NON mergée dans main"
        }
    }
}
catch {
    $mergeDetail = "Erreur lors de la vérification de merge : $($_.Exception.Message)"
    $critical = $true
}

# 3. Vérification que le worktree est bien un dépôt git valide
$isGitRepo = $false
try {
    $revParse = & git -C $WorktreePath rev-parse --is-inside-work-tree 2>&1 | Out-String | ForEach-Object { $_.Trim() }
    $isGitRepo = ($revParse -eq "true")
}
catch {
    $isGitRepo = $false
    $critical = $true
}

$report = [PSCustomObject]@{
    Timestamp      = $timestamp
    WorktreePath   = $WorktreePath
    RepoPath       = $RepoPath
    BranchName     = $BranchName
    SessionId      = $SessionId
    CurrentBranch  = $currentBranch
    BranchMatch    = ($currentBranch -eq $BranchName)
    IsGitRepo      = $isGitRepo
    MergedInMain   = $mergedInMain
    MergeDetail    = $mergeDetail
    Status         = if (-not $critical -and $isGitRepo -and $mergedInMain) { "OK" } else { "DEGRADED" }
    Detail         = $mergeDetail
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WGSA] audit git worktree=$WorktreePath branche=$currentBranch mergéeDansMain=$mergedInMain statut=$($report.Status) critique=$critical"

if ($critical) {
    exit 1
}
exit 0
