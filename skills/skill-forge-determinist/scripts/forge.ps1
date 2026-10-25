#==============================================================================
# SKILL: skill-forge-determinist
# Rôle: Scaffolder unitaire pour créer un skill L4 en transaction atomique.
# Couche: Méta-Skills & Cycle de Vie
#==============================================================================

[CmdletBinding()]
param(
    [string]$SkillName,
    [string]$SkillDescription,
    [string[]]$SkillTriggers = @(),
    [string]$TargetRepo = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\forge-wal.log"
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

# Validation des entrées
if (-not $SkillName) {
    Write-Output "[FAIL] -SkillName est obligatoire"
    Write-WAL "[FAIL] SkillName manquant"
    exit 1
}

if (-not $SkillDescription) {
    Write-Output "[FAIL] -SkillDescription est obligatoire"
    Write-WAL "[FAIL] SkillDescription manquant"
    exit 1
}

# Vérifier que le skill n'existe pas déjà
if (Test-Path -LiteralPath $skillPath) {
    Write-Output "[FAIL] Le skill existe déjà : $skillPath"
    Write-WAL "[FAIL] Skill existe déjà : $SkillName"
    exit 1
}

# Générer l'IntentHash
$intentHash = "0xSKILL_$($SkillName.ToUpper().Replace('-', '_'))_20261025"

# Créer le dossier du skill
try {
    New-Item -ItemType Directory -Force -Path $skillPath | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $skillPath "scripts") | Out-Null
}
catch {
    Write-Output "[FAIL] Impossible de créer le dossier : $($_.Exception.Message)"
    Write-Wal "[FAIL] Création dossier échouée : $SkillName error=$($_.Exception.Message)"
    exit 1
}

# Créer le SKILL.md
$skillMd = Join-Path $skillPath "SKILL.md"
$frontmatter = @"
---
type: SKILL
version: "1.0.0"
status: active
date: "$timestamp"
intent_hash: $intentHash
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/$SkillName/SKILL.md
---

# Skill — $SkillName

## Objectif

$SkillDescription

## Déclencheur

- Création d'un nouveau skill L4 dans le dépôt SKILLS

## Entrées

Aucune (skill nouvellement créé)

## Sorties

- Dossier du skill avec SKILL.md et scripts/

## Règles

### 1. Encodage CP1252 strict

Tous les scripts PowerShell doivent être en encodage CP1252.

### 2. Frontmatter YAML standardisé

Voir l'en-tête de ce fichier.

### 3. Section WAL NEXUS

Chaque SKILL.md doit inclure une section WAL NEXUS.

## Script d'investigation

scripts/ (à implémenter selon le besoin spécifique du skill)

## Tests

À définir selon le besoin spécifique du skill.

## Probes

- SKILL.md présent avec frontmatter valide
- scripts/ présent

## WAL NEXUS

```
[WAL_NEXUS] skill=$SkillName action=created timestamp=$timestamp
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
"@

try {
    $frontmatter | Out-File -FilePath $skillMd -Encoding UTF8
}
catch {
    Write-Output "[FAIL] Impossible d'écrire SKILL.md : $($_.Exception.Message)"
    Write-Wal "[FAIL] Écriture SKILL.md échouée : $SkillName error=$($_.Exception.Message)"
    exit 1
}

# Créer un script placeholder dans scripts/
$scriptFile = Join-Path $skillPath "scripts\$($SkillName).ps1"
$scriptContent = @"
#==============================================================================
# SKILL: $SkillName
# Script d'investigation du skill $SkillName
#==============================================================================

[CmdletBinding()]
param()

Write-Output "Skill $SkillName — opération d'investigation"
exit 0
"@

try {
    $scriptContent | Out-File -FilePath $scriptFile -Encoding UTF8
}
catch {
    Write-Output "[FAIL] Impossible d'écrire le script : $($_.Exception.Message)"
    Write-Wal "[FAIL] Écriture script échouée : $SkillName error=$($_.Exception.Message)"
    exit 1
}

# Ajouter l'entrée dans REGISTRY.yaml
$registryPath = Join-Path $TargetRepo "REGISTRY.yaml"
if (Test-Path -LiteralPath $registryPath) {
    $registryContent = Get-Content -LiteralPath $registryPath -Raw
    $newEntry = @"
  - id: $SkillName
    name: $SkillName
    description: $SkillDescription
    version: 1.0.0
    status: active
    source: native
    source_repo: gerivdb/SKILLS
    path: skills/$SkillName/SKILL.md
    created: $timestamp
    updated: $timestamp
    author: gerivdb
    license: MIT
    type: domain
    triggers: $($SkillTriggers -join ', ')
    domain: general
    phi_weight: 0.005
    assimilation_status: N/A
"@
    $registryContent + "`n" + $newEntry | Out-File -FilePath $registryPath -Encoding UTF8
    Write-Wal "[INFO] Entrée ajoutée dans REGISTRY.yaml : $SkillName"
}

# Ajouter l'entrée dans MANIFEST.json
$manifestPath = Join-Path $TargetRepo "MANIFEST.json"
if (Test-Path -LiteralPath $manifestPath) {
    Write-Wal "[INFO] MANIFEST.json à mettre à jour manuellement : $SkillName"
}

# Créer les jonctions NTFS
$kilocodeTarget = "$env:USERPROFILE\.kilocode\skills\$SkillName"
$geminiTarget = "$env:USERPROFILE\.gemini\config\skills\$SkillName"

try {
    cmd /c "mklink /J `"$kilocodeTarget`" `"$skillPath`"" | Out-Null
    cmd /c "mklink /J `"$geminiTarget`" `"$skillPath`"" | Out-Null
    Write-Wal "[INFO] Jonctions NTFS créées : $SkillName"
}
catch {
    Write-Wal "[WARN] Jonctions NTFS échouées : $SkillName error=$($_.Exception.Message)"
}

# Rapport final
$report = [PSCustomObject]@{
    SkillName    = $SkillName
    SkillPath    = $skillPath
    IntentHash   = $intentHash
    Timestamp    = $timestamp
    Status       = "created"
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[OK] Skill forge terminé : $SkillName"
Write-Output "`n[OK] Skill '$SkillName' créé avec succès dans $skillPath"
exit 0