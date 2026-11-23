#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Génère skills-index.json avec scoring pondéré des triggers (Phase 5, T041-T045).

.DESCRIPTION
    Scanne le dossier skills/, extrait le frontmatter YAML de chaque SKILL.md,
    calcule un score de base par skill (nombre de triggers × poids moyen),
    et produit skills-index.json utilisé par skill-router.ps1 pour le
    routage inter-shards.

.PARAMETER SkillsRoot
    Répertoire racine des skills.

.PARAMETER OutputPath
    Chemin du fichier skills-index.json à générer.

.EXAMPLE
    ./index-skills.ps1
#>

[CmdletBinding()]
param(
    [string]$SkillsRoot = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills",
    [string]$OutputPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime()

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $SkillsRoot)) {
    Write-Error "Répertoire skills introuvable : $SkillsRoot"
    exit 1
}
$skillsRootParent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $skillsRootParent)) {
    New-Item -ItemType Directory -Force -Path $skillsRootParent | Out-Null
}

# --- Extraction du frontmatter YAML ---
function Extract-YamlFrontmatter {
    param([string]$FilePath)
    $content = Get-Content -LiteralPath $FilePath -Raw -ErrorAction Stop
    $content = $content -replace "^\xEF\xBB\xBF", "" -replace "`r`n", "`n"
    $match = [regex]::Match($content, '^---\s*\n(.*?)\n---', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if (-not $match.Success) { return $null }
    $yamlText = $match.Groups[1].Value
    $result = @{}
    $prevKey = $null
    foreach ($line in $yamlText -split "`n") {
        if ($line -match '^(\w+):\s*(.*)$') {
            $key = $matches[1]
            $value = $matches[2].Trim().Trim('"')
            $result[$key] = $value
            $prevKey = $key
        }
        elseif ($line -match '^\s*-\s*(.*)$') {
            $listName = $prevKey
            if (-not $result.ContainsKey($listName)) { $result[$listName] = @() }
            $result[$listName] += $matches[1].Trim().Trim('"')
        }
    }
    return $result
}

# --- Score de base d'un skill ---
function Calc-BaseScore {
    param([array]$Triggers, [array]$Weights)
    $count = $Triggers.Count
    if ($count -eq 0) { return 0 }
    if ($Weights -and $Weights.Count -gt 0) {
        $sum = 0
        $i = 0
        foreach ($w in $Weights) {
            if ($w -match '^\d+$') { $sum += [int]$w }
            $i++
        }
        return [math]::Round($sum / $count, 2)
    }
    return [math]::Round($count, 2)
}

# --- Scan des skills ---
$index = @{
    generated_at_utc = $nowUtc.ToString("o")
    source_repo = $SkillsRoot
    total_skills = 0
    active_skills = 0
    draft_skills = 0
    skills = @()
}

$skillFolders = Get-ChildItem -LiteralPath $SkillsRoot -Directory -ErrorAction SilentlyContinue
foreach ($folder in $skillFolders) {
    $skillFile = Join-Path $folder.FullName "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile)) {
        Write-Warning "SKILL.md absent dans $($folder.Name), ignoré."
        continue
    }

    $fm = Extract-YamlFrontmatter -FilePath $skillFile
    if ($null -eq $fm) {
        Write-Warning "Frontmatter YAML invalide dans $skillFile, ignoré."
        continue
    }

    $fileBytes = [System.IO.File]::ReadAllBytes($skillFile)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $hashBytes = $sha256.ComputeHash($fileBytes)
    $hashString = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''

    $triggers = @($fm.triggers)
    $weights = @($fm.weight)
    $antiTriggers = @($fm.anti_triggers)
    $tags = @($fm.tags)
    $supersedes = @($fm.supersedes)

    $baseScore = Calc-BaseScore -Triggers $triggers -Weights $weights

    $skillEntry = [PSCustomObject]@{
        name = $fm.name
        version = $fm.version
        status = $fm.status
        type = $fm.type
        category = $fm.category
        intent_hash = $fm.intent_hash
        provenance = $fm.provenance
        source_shard = $fm.source_shard
        path = "skills/$($folder.Name)"
        triggers = $triggers
        anti_triggers = $antiTriggers
        weight = $weights
        base_score = $baseScore
        tags = $tags
        hash_sha256 = $hashString
        created_at = $fm.created_at
        updated_at = $fm.updated_at
        supersedes = $supersedes
        superseded_by = $fm.superseded_by
    }

    $index.skills += $skillEntry
    $index.total_skills++
    if ($fm.status -eq "active") { $index.active_skills++ }
    elseif ($fm.status -eq "draft") { $index.draft_skills++ }
}

# --- Trier par score décroissant ---
$index.skills = $index.skills | Sort-Object base_score -Descending

# --- Écriture de l'index ---
$indexJson = $index | ConvertTo-Json -Depth 5
Set-Content -LiteralPath $OutputPath -Value $indexJson -Encoding UTF8

Write-Output "=============================================="
Write-Output "Index des skills généré (avec scoring)"
Write-Output "=============================================="
Write-Output "Fichier      : $OutputPath"
Write-Output "Total        : $($index.total_skills)"
Write-Output "Actifs       : $($index.active_skills)"
Write-Output "Brouillons   : $($index.draft_skills)"
Write-Output "Généré le    : $($index.generated_at_utc)"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
}
