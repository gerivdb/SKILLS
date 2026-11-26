#!/usr/bin/env pwsh
# index-skills.ps1 — Régénération de skills-index.json (ENV3)
# Scanne le dossier D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/ et reconstruit
# skills-index.json à partir des frontmatter YAML des SKILL.md.
#
# Usage :
#   .\index-skills.ps1
#
# Sortie : skills-index.json mis à jour sur disque.

$ErrorActionPreference = "Stop"

$SKILLS_DIR = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
$SKILLS_INDEX = "$SKILLS_DIR\skills-index.json"

if (-not (Test-Path -LiteralPath $SKILLS_DIR)) {
    Write-Output "ERREUR: dossier SKILLS introuvable: $SKILLS_DIR"
    exit 1
}

$dossiers = Get-ChildItem -LiteralPath $SKILLS_DIR -Directory | Where-Object { $_.Name -notmatch '^__|^\.' }

$skills = @{}

foreach ($d in $dossiers) {
    $skillMd = "$($d.FullName)\SKILL.md"
    if (-not (Test-Path -LiteralPath $skillMd)) {
        continue
    }

    $contenu = Get-Content -LiteralPath $skillMd -Raw
    if ($contenu -notmatch '^---\s*$([\s\S]*?)^---\s*$') {
        continue
    }

    $frontmatter = $Matches[1]

    function Get-YamlValeur($texte, $cle) {
        if ($texte -match ($cle + ':\s*(.+)')) {
            return $Matches[1].Trim().Trim('"')
        }
        return $null
    }

    $nom = Get-YamlValeur $frontmatter 'name'
    if (-not $nom) { $nom = $d.Name }

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
    $entree['path'] = $d.Name
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
