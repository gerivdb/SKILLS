#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Boucle de retour et mesure d'usage des skills (Phase 6, T051-T060).

.DESCRIPTION
    Enregistre le résultat d'exécution d'un skill (succès/échec/contourné)
    dans son EVIDENCE.md, met à jour le score d'utilité, et signale les
    skills morts (score sous seuil) pour révision ou dépréciation.

.PARAMETER SkillName
    Nom du skill dont on enregistre le résultat.

.PARAMETER Result
    Résultat : succès | echec | contourné.

.PARAMETER ShardId
    Identifiant du shard d'exécution (défaut: ENV2).

.PARAMETER RootCause
    Cause racine en cas d'échec (facultatif).

.PARAMETER SkillsRoot
    Répertoire racine des skills.

.EXAMPLE
    ./skill-feedback.ps1 -SkillName chromium-profile-2 -Result succes -ShardId ENV2

.EXAMPLE
    ./skill-feedback.ps1 -SkillName cdp-profile-2 -Result echec -ShardId ENV2 -RootCause "Port 9222 non répondant"

.NOTES
    Intégration: SPEC-SKILL-FORMAT.md section 5.1 (Boucle de retour)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("succes", "echec", "contourne")]
    [string]$Result,

    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [string]$ShardId = "ENV2",

    [string]$RootCause,

    [string]$SkillsRoot = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
$skillFolder = Join-Path $SkillsRoot $SkillName
if (-not (Test-Path -LiteralPath $skillFolder)) {
    Write-Error "Skill introuvable : $skillFolder"
    exit 1
}

$skillFile = Join-Path $skillFolder "SKILL.md"
$evidenceFile = Join-Path $skillFolder "EVIDENCE.md"
$historyFile = Join-Path $skillFolder "HISTORY.md"

if (-not (Test-Path -LiteralPath $skillFile)) {
    Write-Error "SKILL.md introuvable : $skillFile"
    exit 1
}

# --- Lecture du skill actuel ---
$skillContent = Get-Content -LiteralPath $skillFile -Raw -ErrorAction Stop
$skillContent = $skillContent -replace "^\xEF\xBB\xBF", "" -replace "`r`n", "`n"

function Extract-YamlValueSimple {
    param([string]$Content, [string]$Key)
    $match = [regex]::Match($Content, "(?m)^${key}:\s*(.+)$")
    if ($match.Success) { return $match.Groups[1].Value.Trim().Trim('"') }
    return $null
}

$currentVersion = Extract-YamlValueSimple -Content $skillContent -Key "version"
$currentScore = Extract-YamlValueSimple -Content $skillContent -Key "utility_score"
if (-not $currentScore -or $currentScore -eq "") { $currentScore = 0 }

# --- Mise à jour du score d'utilité ---
$scoreDelta = 0
switch ($Result) {
    "succes" { $scoreDelta = +1 }
    "echec"  { $scoreDelta = -2 }
    "contourne" { $scoreDelta = -1 }
}
$newScore = [int]$currentScore + $scoreDelta
if ($newScore -lt -10) { $newScore = -10 }  # plancher

# --- Écriture dans EVIDENCE.md ---
if (-not (Test-Path -LiteralPath $evidenceFile)) {
    $evidenceContent = "# Preuve d'exécution — $SkillName`n`n"
    Set-Content -LiteralPath $evidenceFile -Value $evidenceContent -Encoding UTF8
}

$evidenceContent = Get-Content -LiteralPath $evidenceFile -Raw -ErrorAction SilentlyContinue
if (-not $evidenceContent) { $evidenceContent = "# Preuve d'exécution — $SkillName`n`n" }

$evidenceEntry = @"
### $nowUtc | Shard: $ShardId | Résultat: $Result | Score utilité: $currentScore → $newScore
$(if ($RootCause) { "- Cause racine : $RootCause`n" })
"@

$evidenceContent = $evidenceContent.TrimEnd() + "`n" + $evidenceEntry
Set-Content -LiteralPath $evidenceFile -Value $evidenceContent -Encoding UTF8

# --- Mise à jour du score dans SKILL.md ---
$skillContent = $skillContent -replace '(?m)^utility_score:.*$', "utility_score: $newScore"
if ($skillContent -notmatch '(?m)^utility_score:') {
    # Ajouter le champ s'il n'existe pas
    $skillContent = $skillContent -replace '(?m)^updated_at:.*$', "updated_at: `"$nowUtc`"`nutility_score: $newScore"
} else {
    $skillContent = $skillContent -replace '(?m)^updated_at:.*$', "updated_at: `"$nowUtc`""
}
Set-Content -LiteralPath $skillFile -Value $skillContent -Encoding UTF8

# --- Mise à jour HISTORY.md ---
if (Test-Path -LiteralPath $historyFile) {
    $historyContent = Get-Content -LiteralPath $historyFile -Raw
    $historyEntry = "`n`n## Feedback — $nowUtc`n- Résultat: $Result | Shard: $ShardId | Score utilité: $currentScore → $newScore`n"
    if ($RootCause) { $historyEntry += "- Cause racine : $RootCause`n" }
    $historyContent = $historyContent.TrimEnd() + $historyEntry
    Set-Content -LiteralPath $historyFile -Value $historyContent -Encoding UTF8
}

# --- Détection skill mort (score sous seuil -5) ---
$deadSkill = $false
if ($newScore -le -5) {
    $deadSkill = $true
    $warnings += "SKILL_MORT: $SkillName a un score utilité de $newScore (≤ -5). Révision ou dépréciation requise."
}

# --- Rapport ---
Write-Output "=============================================="
Write-Output "BOUCLE DE RETOUR — $SkillName"
Write-Output "=============================================="
Write-Output "Résultat     : $Result"
Write-Output "Shard        : $ShardId"
Write-Output "Score avant  : $currentScore"
Write-Output "Score après  : $newScore"
Write-Output "Évidence     : $evidenceFile"
Write-Output "=============================================="

if ($deadSkill) {
    Write-Output "ALERTE : Skill mort détecté. Action requise : révision via distill-skill.ps1 --base-skill $SkillName ou archivage."
}

if ($warnings.Count -gt 0) {
    foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
}

Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
}
