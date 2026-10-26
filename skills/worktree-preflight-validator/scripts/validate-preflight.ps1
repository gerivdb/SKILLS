#==============================================================================
# SKILL: worktree-preflight-validator
# Rôle: Vérification pré-vol atomique avant naissance d'un worktree managé.
#       Lecture seule (Read-Only). Fail-closed sur toute anomalie critique.
# Couche Worktree Engineering - Pre-vol
#==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$WorktreePath,
    [Parameter(Mandatory)] [string]$RepoPath,
    [int]$MinFreeSpaceMB = 100
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal"
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath "$logDir\wpv-wal.log" -Append -Encoding UTF8
}

$critical = $false
$checks = @()

# --- 1. Version PowerShell 7+ ---
$psOk = $false
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $psOk = $true
} else {
    $critical = $true
}
$checks += [PSCustomObject]@{
    Check    = "PowerShell version"
    Status   = if ($psOk) { "OK" } else { "CRITICAL" }
    Detail   = "Version détectée : $($PSVersionTable.PSVersion) (requis >= 7)"
    Critical = $psOk -eq $false
}

# --- 2. Espace disque NTFS sur le volume du worktree ---
$diskOk = $false
$diskRoot = Split-Path $WorktreePath -Qualifier
if ($diskRoot) {
    try {
        $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$diskRoot'" | Select-Object -First 1
        if ($disk -and $disk.FreeSpace -ge ($MinFreeSpaceMB * 1MB)) {
            $diskOk = $true
        } else {
            $critical = $true
        }
    }
    catch {
        $critical = $true
    }
} else {
    $critical = $true
}
$freeMB = if ($disk) { [math]::Round($disk.FreeSpace / 1MB) } else { 0 }
$checks += [PSCustomObject]@{
    Check    = "Espace disque NTFS"
    Status   = if ($diskOk) { "OK" } else { "CRITICAL" }
    Detail   = "Libre sur $diskRoot : $freeMB Mo (seuil : $MinFreeSpaceMB Mo)"
    Critical = $diskOk -eq $false
}

# --- 3. Validité des chemins d'entrée (chemin littéral) ---
$wtPathOk = (Test-Path -LiteralPath $WorktreePath)
$repoPathOk = (Test-Path -LiteralPath $RepoPath)
if (-not $wtPathOk -or -not $repoPathOk) { $critical = $true }
$checks += [PSCustomObject]@{
    Check    = "Chemins d'entrée"
    Status   = if ($wtPathOk -and $repoPathOk) { "OK" } else { "CRITICAL" }
    Detail   = "WORKTREE_PATH=$($wtPathOk) REPO_PATH=$($repoPathOk)"
    Critical = (-not $wtPathOk -or -not $repoPathOk)
}

# --- 4. Existence des 5 skills cibles du hook de naissance ---
$skillsRoot = Join-Path (Split-Path (Split-Path $RepoPath -Parent) -Parent) "L4-TOOLS\SKILLS\skills"
$targetSkills = @(
    "worktree-zero-copy-hydrator\scripts\hydrate.ps1",
    "worktree-genetic-contractor\scripts\contract.ps1",
    "worktree-synaptic-bus-joiner\scripts\join_bus.ps1",
    "worktree-precommit-armorer\scripts\armor.ps1",
    "worktree-lifecycle-reaper\scripts\reap.ps1"
)
$skillsOk = $true
$skillsDetail = @()
foreach ($rel in $targetSkills) {
    $full = Join-Path $skillsRoot $rel
    $exists = Test-Path -LiteralPath $full
    if (-not $exists) { $skillsOk = $false; $critical = $true }
    $skillsDetail += "$rel : $exists"
}
$checks += [PSCustomObject]@{
    Check    = "Skills cibles présents"
    Status   = if ($skillsOk) { "OK" } else { "CRITICAL" }
    Detail   = ($skillsDetail -join "; ")
    Critical = $skillsOk -eq $false
}

# --- Rapport JSON structuré ---
$report = [PSCustomObject]@{
    Timestamp     = $timestamp
    WorktreePath  = $WorktreePath
    RepoPath      = $RepoPath
    MinFreeSpaceMB= $MinFreeSpaceMB
    Critical      = $critical
    Checks        = $checks
    Status        = if ($critical) { "FAIL" } else { "OK" }
}

$report | ConvertTo-Json -Depth 4

Write-Wal "[WPV] preflight worktree=$WorktreePath statut=$($report.Status) critique=$critical"

if ($critical) {
    exit 1
}
exit 0
