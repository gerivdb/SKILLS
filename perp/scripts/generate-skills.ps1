# ============================================================
# generate-skills.ps1
# Génération d'un ZIP de Skills Perplexity au format canonique
# Repo   : gerivdb/SKILLS
# Chemin : perp/scripts/generate-skills.ps1
# Format : UTF-8 sans BOM, front-matter YAML strict
# ============================================================
$ErrorActionPreference = "Stop"
$tempDir = Join-Path $env:TEMP "SkillsTemp"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# ------------------------------------------------------------
# Fonction d'écriture d'un skill au format canonique
# ------------------------------------------------------------
function Write-Skill {
    param(
        [string]$FileName,          # ex: "mon-skill.md"
        [string]$Name,              # ex: "mon-skill" (kebab-case strict)
        [string]$Title,             # ex: "Mon Skill"
        [string]$DescriptionLine1,  # ex: "Description courte du rôle."
        [string[]]$Keywords,        # ex: @("mot1", "mot2")
        [string]$Body               # Corps complet (Instructions, Règles, Format, Exemples)
    )
    $keywordsFormatted = ($Keywords | ForEach-Object { '"' + $_ + '"' }) -join ", "
    $yaml = @"
---
name: $Name
description: $DescriptionLine1 Use when user mentions
  $keywordsFormatted.
---

# $Title

$Body
"@
    $path = Join-Path $tempDir $FileName
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($path, $yaml, $utf8NoBom)
    Write-Host "  OK $FileName"
}

# ============================================================
# Corps des skills (here-strings @' '@)
# Dupliquer ce bloc pour chaque skill
# ============================================================
$bodySkill1 = @'
## Instructions

1. **Identifier la demande** : contexte et périmètre.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `<dépôt>`.
3. **Appliquer les tags NEXUS**.
4. **Répondre en français**.

## Règles

- Règle canonique 1.
- Ne pas inventer de commandes sans preuve.

## Format

- Format de sortie 1.

## Exemples

- "[Déclencheur typique]" → Action concrète.
'@

# ============================================================
# Appels — un Write-Skill par skill à générer
# ============================================================
Write-Host "Génération des skills..."
Write-Skill `
    "skill-exemple.md" `
    "skill-exemple" `
    "Skill Exemple" `
    "Description courte du rôle." `
    @("mot-clé1", "mot-clé2", "mot-clé3") `
    $bodySkill1

# ============================================================
# Vérification et compression
# ============================================================
$files = Get-ChildItem -Path $tempDir -Filter *.md
Write-Host "Fichiers générés : $($files.Count)"
if ($files.Count -eq 0) {
    Write-Error "Aucun fichier généré. Abandon."
    exit 1
}

# Destination : Bureau ou TEMP si inaccessible
$desktop = [Environment]::GetFolderPath("Desktop")
if (-not $desktop -or -not (Test-Path $desktop)) { $desktop = $env:TEMP }
$zip = Join-Path $desktop "Skills.zip"

Compress-Archive -Path (Join-Path $tempDir '*.md') -DestinationPath $zip -Force
Write-Host "ZIP créé : $zip"
Write-Host "Importer ce ZIP dans Perplexity > Space > Skills."

# Nettoyage
Remove-Item -Path $tempDir -Recurse -Force
