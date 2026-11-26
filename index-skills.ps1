#!/usr/bin/env pwsh
# index-skills.ps1 — Régénération de skills-index.json (ENV3)
# Scanne le dossier D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/ et reconstruit
# skills-index.json à partir des frontmatter YAML des SKILL.md.
# Supporte l'arborescence imbriquée (sous-dossiers thématiques).
#
# Usage :
#   .\index-skills.ps1
#
# Sortie : skills-index.json mis à jour sur disque.

$ErrorActionPreference = "Continue"

$SKILLS_DIR = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
$SKILLS_INDEX = "$SKILLS_DIR\skills-index.json"

if (-not (Test-Path -LiteralPath $SKILLS_DIR)) {
    Write-Output "ERREUR: dossier SKILLS introuvable: $SKILLS_DIR"
    exit 1
}

# Trouve tous les SKILL.md de façon récursive, en excluant les dossiers système
$skillFiles = Get-ChildItem -LiteralPath $SKILLS_DIR -Filter "SKILL.md" -Recurse | Where-Object {
    $parent = $_.Directory.Name
    $parent -notmatch '^__|^\.'
}

function Get-YamlValeur {
    param([string]$texte, [string]$cle)
    if ($texte -match ($cle + ':\s*(.+)')) {
        return $Matches[1].Trim().Trim('"')
    }
    return $null
}

function Test-Frontmatter {
    param([string]$contenu)
    # Vérifie que le contenu commence par --- sur une ligne, puis trouve le --- de clôture
    $lines = $contenu -split "`n"
    if ($lines[0].Trim() -ne '---') {
        return $false
    }
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Trim() -eq '---') {
            return $true
        }
        if ($i -gt 50) { break }
    }
    return $false
}

function Extract-Frontmatter {
    param([string]$contenu)
    $lines = $contenu -split "`n"
    $fmLines = @()
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Trim() -eq '---') {
            break
        }
        $fmLines += $lines[$i]
    }
    return ($fmLines -join "`n")
}

$skills = @{}

foreach ($f in $skillFiles) {
    $skillMd = $f.FullName
    $skillDir = $f.Directory

    $contenu = Get-Content -LiteralPath $skillMd -Raw -ErrorAction SilentlyContinue
    if (-not $contenu) { continue }

    if (-not (Test-Frontmatter $contenu)) { continue }

    $frontmatter = Extract-Frontmatter $contenu

    $nom = Get-YamlValeur $frontmatter 'name'
    if (-not $nom) { $nom = $skillDir.Name }

    # Le path est le chemin relatif depuis SKILLS_DIR
    $relPath = $skillDir.FullName.Substring($SKILLS_DIR.Length).TrimStart('\').TrimStart('/')
    
    $entree = [ordered]@{}
    $entree['name'] = $nom
    $entree['type'] = Get-YamlValeur $frontmatter 'type'
    $entree['version'] = Get-YamlValeur $frontmatter 'version'
    $entree['status'] = Get-YamlValeur $frontmatter 'status'
    $entree['date'] = Get-YamlValeur $frontmatter 'date'
    $entree['intent_hash'] = Get-YamlValeur $frontmatter 'intent_hash'
    $entree['layer'] = Get-YamlValeur $frontmatter 'layer'
    $entree['author'] = Get-YamlValeur $frontmatter 'author'
    $entree['source_repo'] = Get-YamlValeur $frontmatter 'source_repo'
    $entree['source_path'] = Get-YamlValeur $frontmatter 'source_path'
    $entree['path'] = $relPath
    $entree['description'] = Get-YamlValeur $frontmatter 'description'
    $entree['trigger'] = Get-YamlValeur $frontmatter 'trigger'

    # Nettoyer les valeurs nulles
    $entreePropre = [ordered]@{}
    foreach ($cle in $entree.Keys) {
        if ($entree[$cle] -ne $null -and $entree[$cle] -ne '') {
            $entreePropre[$cle] = $entree[$cle]
        }
    }

    $skills[$nom] = $entreePropre
}

$index = [ordered]@{}
$index['generated_at_utc'] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss.ffffffZ")
$index['skills'] = $skills

$json = $index | ConvertTo-Json -Depth 3
Set-Content -LiteralPath $SKILLS_INDEX -Value $json -Encoding UTF8

Write-Output ("INDEX: " + $skills.Count + " skills indexes dans " + $SKILLS_INDEX)
exit 0
