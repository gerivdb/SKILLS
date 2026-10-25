#==============================================================================
# SKILL: skill-pruner-retire
# Rôle: Décommissionne proprement un skill ou un Combo obsolète.
# Couche: Méta-Skills & Cycle de Vie
#==============================================================================

[CmdletBinding()]
param(
    [string]$SkillName,
    [switch]$Archive = $true,
    [switch]$CleanRegistry = $true,
    [switch]$CleanJunctions = $true,
    [string]$ArchiveRoot = "D:\DO\WEB\TOOLS\L5-ARCHIVE\skills",
    [string]$TargetRepo = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\prune-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$skillPath = Join-Path $TargetRepo "skills" $SkillName

function Write-WAL {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# Validation
if (-not $SkillName) {
    Write-Output "[FAIL] -SkillName est obligatoire"
    Write-Wal "[FAIL] SkillName manquant"
    exit 1
}

if (-not (Test-Path -LiteralPath $skillPath)) {
    Write-Output "[FAIL] Le skill n'existe pas : $skillPath"
    Write-Wal "[FAIL] Skill introuvable : $SkillName"
    exit 1
}

# Vérifier qu'aucun Combo ne dépend de ce skill (via weave)
# (Heuristique simple : vérifier si le nom du skill apparaît comme sortie d'un autre skill)
$skillDirs = Get-ChildItem -LiteralPath (Join-Path $TargetRepo "skills") -Directory | Where-Object {
    $_.Name -ne $SkillName -and (Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md"))
}
$referencedBy = @()
foreach ($d in $skillDirs) {
    $content = Get-Content -LiteralPath (Join-Path $d.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue
    if ($content -match $SkillName) {
        $referencedBy += $d.Name
    }
}

if ($referencedBy.Count -gt 0) {
    Write-Output "[WARN] Le skill $SkillName est référencé par : $($referencedBy -join ', ')"
    Write-Output "[WARN] Retrait annulé pour éviter de casser les Combos dépendants"
    Write-Wal "[WARN] Retrait annulé : $SkillName référencé par $($referencedBy -join ', ')"
    exit 0
}

# Archivage
$archived = $false
if ($Archive) {
    if (-not (Test-Path -LiteralPath $ArchiveRoot)) {
        New-Item -ItemType Directory -Force -Path $ArchiveRoot | Out-Null
    }
    $archivePath = Join-Path $ArchiveRoot $SkillName
    try {
        Move-Item -LiteralPath $skillPath -Destination $archivePath -Force
        $archived = $true
        Write-Wal "[INFO] Skill archivé : $SkillName -> $archivePath"
    }
    catch {
        Write-Output "[FAIL] Échec de l'archivage : $($_.Exception.Message)"
        Write-Wal "[FAIL] Archivage échoué : $SkillName error=$($_.Exception.Message)"
        exit 1
    }
}
else {
    try {
        Remove-Item -LiteralPath $skillPath -Recurse -Force
        Write-Wal "[INFO] Skill supprimé : $SkillName"
    }
    catch {
        Write-Output "[FAIL] Échec de la suppression : $($_.Exception.Message)"
        Write-Wal "[FAIL] Suppression échouée : $SkillName error=$($_.Exception.Message)"
        exit 1
    }
}

# Nettoyage des jonctions NTFS
if ($CleanJunctions) {
    $kilocodeLink = "$env:USERPROFILE\.kilocode\skills\$SkillName"
    $geminiLink = "$env:USERPROFILE\.gemini\config\skills\$SkillName"
    
    foreach ($link in @($kilocodeLink, $geminiLink)) {
        if (Test-Path -LiteralPath $link) {
            try {
                Remove-Item -LiteralPath $link -Recurse -Force
                Write-Wal "[INFO] Jonction supprimée : $link"
            }
            catch {
                Write-Wal "[WARN] Échec suppression jonction : $link error=$($_.Exception.Message)"
            }
        }
    }
}

# Nettoyage des registres
if ($CleanRegistry) {
    $registryPath = Join-Path $TargetRepo "REGISTRY.yaml"
    if (Test-Path -LiteralPath $registryPath) {
        $content = Get-Content -LiteralPath $registryPath -Raw
        # Retirer l'entrée du skill (heuristique : bloc commençant par "- id: $SkillName" ou "- name: $SkillName")
        $lines = $content -split "`n"
        $newLines = @()
        $skip = $false
        foreach ($line in $lines) {
            if ($line -match "^\s*-\s*(id|name):\s*$SkillName\s*$") {
                $skip = $true
                continue
            }
            if ($skip -and $line -match "^\s*-\s+(id|name):") {
                $skip = $false
                $newLines += $line
                continue
            }
            if (-not $skip) {
                $newLines += $line
            }
        }
        $newLines -join "`n" | Out-File -FilePath $registryPath -Encoding UTF8
        Write-Wal "[INFO] REGISTRY.yaml nettoyé : $SkillName"
    }
}

# Rapport final
$report = [PSCustomObject]@{
    SkillName   = $SkillName
    Archived    = $archived
    Timestamp   = $timestamp
    Status      = "pruned"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[OK] Skill pruné : $SkillName archived=$archived"
Write-Output "`n[OK] Skill '$SkillName' retiré avec succès"
exit 0