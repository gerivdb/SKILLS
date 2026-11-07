#==============================================================================
# SKILL: worktree-junction-validator
# Rôle: Valider l'intégrité des jonctions NTFS (node_modules, .venv, .cache/pip)
# d'un worktree en lecture seule (Read-Only).
# Couche Worktree Engineering — Diagnostic
#==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$WorktreePath,
    [Parameter(Mandatory)] [string]$RepoPath
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wjv-wal.log" -Append -Encoding UTF8
}

if (-not $WorktreePath -or -not (Test-Path -LiteralPath $WorktreePath)) {
    Write-Output "[FAIL] -WorktreePath invalide ou introuvable : $WorktreePath"
    Write-Wal "[FAIL] WorktreePath invalide : $WorktreePath"
    exit 1
}

$cacheDirs = @("node_modules", ".venv", ".cache/pip")
$results = @()
$critical = $false

foreach ($cacheDir in $cacheDirs) {
    $target = Join-Path $WorktreePath $cacheDir
    $source = Join-Path $RepoPath $cacheDir

    if (-not (Test-Path -LiteralPath $target)) {
        $results += [PSCustomObject]@{
            Dir       = $cacheDir
            Status    = "ABSENT"
            Detail    = "Aucune jonction ni dossier présent dans le worktree"
            IsJunction = $false
            TargetValid = $false
        }
        continue
    }

    try {
        $item = Get-Item -LiteralPath $target
        $isJunction = ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0

        if (-not $isJunction) {
            $results += [PSCustomObject]@{
                Dir       = $cacheDir
                Status    = "NOT_JUNCTION"
                Detail    = "Présent mais ce n'est pas une jonction NTFS"
                IsJunction = $false
                TargetValid = $false
            }
            continue
        }

        # Vérifier que la cible de la jonction existe
        $targetValid = $false
        $detail = "Jonction valide"
        try {
            # Résoudre la cible via le système de fichiers
            $resolved = $item.Target
            if (-not $resolved) {
                # Tentative via cmd mklink /J lecture indirecte
                $resolved = (Get-Item -LiteralPath $target).FullName
            }
            if (Test-Path -LiteralPath $resolved) {
                $targetValid = $true
            } else {
                $detail = "Cible de jonction introuvable : $resolved"
                $critical = $true
            }
        }
        catch {
            $detail = "Erreur de résolution de la cible : $($_.Exception.Message)"
            $targetValid = $false
            $critical = $true
        }

        $results += [PSCustomObject]@{
            Dir        = $cacheDir
            Status     = if ($targetValid) { "OK" } else { "BROKEN" }
            Detail     = $detail
            IsJunction = $true
            TargetValid= $targetValid
        }
    }
    catch {
        $results += [PSCustomObject]@{
            Dir       = $cacheDir
            Status    = "ERROR"
            Detail    = "Erreur d'inspection : $($_.Exception.Message)"
            IsJunction = $false
            TargetValid = $false
        }
        $critical = $true
    }
}

$report = [PSCustomObject]@{
    Timestamp     = $timestamp
    WorktreePath  = $WorktreePath
    RepoPath      = $RepoPath
    Critical      = $critical
    Junctions     = $results
    CountTotal    = $results.Count
    CountValid    = ($results | Where-Object { $_.Status -eq "OK" }).Count
    CountBroken   = ($results | Where-Object { $_.Status -eq "BROKEN" }).Count
    CountAbsent   = ($results | Where-Object { $_.Status -eq "ABSENT" }).Count
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WJV] validation jonctions worktree=$WorktreePath total=$($report.CountTotal) valides=$($report.CountValid) brisées=$($report.CountBroken) absentes=$($report.CountAbsent) critique=$critical"

if ($critical) {
    exit 1
}
exit 0
