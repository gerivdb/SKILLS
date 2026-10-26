#==============================================================================
# SKILL: worktree-session-cleaner
# Rôle: Nettoyage résiduel post-session (fichiers .tmp, logs anciens).
#       Lecture sélective, jamais de suppression de verrous git.
# Couche Worktree Engineering - Maintenance
#==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$WorktreePath,
    [int]$MaxLogAgeDays = 7,
    [switch]$CleanTmp = $true
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wsc-wal.log" -Append -Encoding UTF8
}

$removed = @()
$kept = @()
$critical = $false

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    $report = [PSCustomObject]@{
        Timestamp   = $timestamp
        WorktreePath= $WorktreePath
        Status      = "FAIL"
        Detail      = "WORKTREE_PATH invalide ou introuvable"
        Removed     = @()
        Kept        = @()
    }
    $report | ConvertTo-Json -Depth 3
    Write-Wal "[WSC] echec worktree=$WorktreePath raison=WORKTREE_PATH invalide"
    exit 1
}

# --- 1. Suppression des fichiers .tmp à la racine du worktree ---
if ($CleanTmp) {
    try {
        $tmpFiles = Get-ChildItem -LiteralPath $WorktreePath -Filter "*.tmp" -File -ErrorAction SilentlyContinue
        foreach ($tmp in $tmpFiles) {
            # Ne jamais toucher aux fichiers sous .git
            if ($tmp.FullName -like "$WorktreePath\.git\*") {
                $kept += $tmp.FullName
                continue
            }
            try {
                Remove-Item -LiteralPath $tmp.FullName -Force -ErrorAction Stop
                $removed += $tmp.FullName
            }
            catch {
                $kept += $tmp.FullName
                Write-Wal "[WSC] echec suppression tmp : $($tmp.FullName)"
            }
        }
    }
    catch {
        $critical = $true
        Write-Wal "[WSC] echec scan fichiers .tmp : $($_.Exception.Message)"
    }
}

# --- 2. Suppression des logs ages dans .kilo\logs du worktree ---
$logDir = Join-Path $WorktreePath ".kilo\logs"
$cutoff = (Get-Date).AddDays(-$MaxLogAgeDays)
if (Test-Path -LiteralPath $logDir) {
    try {
        $logFiles = Get-ChildItem -LiteralPath $logDir -File -ErrorAction SilentlyContinue
        foreach ($log in $logFiles) {
            try {
                $lastWrite = $log.LastWriteTime
                if ($lastWrite -lt $cutoff) {
                    Remove-Item -LiteralPath $log.FullName -Force -ErrorAction Stop
                    $removed += $log.FullName
                } else {
                    $kept += $log.FullName
                }
            }
            catch {
                $kept += $log.FullName
            }
        }
    }
    catch {
        $critical = $true
        Write-Wal "[WSC] echec scan logs : $($_.Exception.Message)"
    }
}

# --- Rapport JSON ---
$report = [PSCustomObject]@{
    Timestamp   = $timestamp
    WorktreePath= $WorktreePath
    MaxLogAgeDays = $MaxLogAgeDays
    CleanTmp    = $CleanTmp
    Critical    = $critical
    Removed     = $removed
    Kept        = $kept
    CountRemoved= $removed.Count
    CountKept   = $kept.Count
    Status      = if ($critical) { "DEGRADED" } else { "OK" }
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WSC] nettoyage worktree=$WorktreePath supprimes=$($report.CountRemoves) conserves=$($report.CountKept) critique=$critical"

if ($critical) {
    exit 1
}
exit 0
