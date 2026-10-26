#==============================================================================
# SKILL: worktree-zero-copy-hydrator
# Rôle: Hydratation instantanée d'un worktree neuf via jonctions NTFS vers le cache partagé du repo maître.
# Couche Worktree Engineering — Hydratation
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreePath = $env:WORKTREE_PATH,
    [string]$RepoPath = $env:REPO_PATH,
    [string[]]$CacheDirs = @("node_modules", ".venv", ".cache/pip")
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wzh-wal.log" -Append -Encoding UTF8
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

$hydrated = @()
$skipped = @()
$spaceSavedMB = 0

foreach ($cacheDir in $CacheDirs) {
    $source = Join-Path $RepoPath $cacheDir
    $target = Join-Path $WorktreePath $cacheDir

    if (-not (Test-Path -LiteralPath $source)) {
        $skipped += [PSCustomObject]@{ Dir = $cacheDir; Reason = "Source introuvable dans le repo maître" }
        continue
    }

    if (Test-Path -LiteralPath $target) {
        $skipped += [PSCustomObject]@{ Dir = $cacheDir; Reason = "Déjà existant dans le worktree" }
        continue
    }

    try {
        # Créer le répertoire parent si nécessaire
        $parent = Split-Path -Parent $target
        if (-not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }

        # Créer la jonction NTFS
        cmd /c "mklink /J `"$target`" `"$source`"" | Out-Null
        $hydrated += $cacheDir

        # Estimer l'espace sauvegardé (approximation)
        try {
            $sourceInfo = Get-Item -LiteralPath $source
            # Approximation : on ne compte pas la taille réelle, on note juste la jonction
        }
        catch {}
    }
    catch {
        $skipped += [PSCustomObject]@{ Dir = $cacheDir; Reason = "Erreur de création : $($_.Exception.Message)" }
    }
}

$report = [PSCustomObject]@{
    Timestamp      = $timestamp
    WorktreePath   = $WorktreePath
    RepoPath       = $RepoPath
    HydratedDirs   = $hydrated
    SkippedDirs    = $skipped
    SpaceSavedMB   = $spaceSavedMB
    CountHydrated  = $hydrated.Count
    CountSkipped   = $skipped.Count
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WZCH] hydrate worktree=$WorktreePath hydrated=$($hydrated.Count) skipped=$($skipped.Count)"

exit 0