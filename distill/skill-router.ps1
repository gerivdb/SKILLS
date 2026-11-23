#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Protocole de rappel inter-shards — routage des skills par mode (Phase 16, T151 à T160).

.DESCRIPTION
    Lit skills-index.json, matche les triggers de la demande contre les skills
    indexés avec scoring pondéré et anti_triggers, filtre selon le mode actif
    (architect, data, bdcp, free), sa write_policy (read_only vs lease_required)
    et son budget FREE (contexte, requêtes).

.PARAMETER Request
    Chaîne de caractères décrivant la demande/tâche à router.

.PARAMETER ModeId
    Mode actif actuel (architect, data, bdcp, free). Défaut: free.

.PARAMETER IndexPath
    Chemin vers skills-index.json.

.PARAMETER MinScore
    Score minimum pour activer un skill (défaut: 1.0).

.PARAMETER MaxResults
    Nombre maximum de skills à retourner (défaut: 3).

.PARAMETER ContextSize
    Taille de contexte en octets pour vérification du budget FREE (défaut: 0).

.EXAMPLE
    ./skill-router.ps1 -Request "piloter chromium sur port 9222" -ModeId bdcp

.EXAMPLE
    ./skill-router.ps1 -Request "écrire un script de test" -ModeId data -ContextSize 5000

.NOTES
    Phase 16, T151 à T160 — Routage de skills par mode
    Dépend : skills-index.json, modes-matrix.json, effective-permissions.json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Request,

    [string]$ModeId = "free",

    [string]$IndexPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json",

    [double]$MinScore = 1.0,

    [int]$MaxResults = 3,

    [int]$ContextSize = 0
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $IndexPath)) {
    Write-Error "Index des skills introuvable : $IndexPath"
    exit 1
}

# --- Lecture de l'index ---
$indexContent = Get-Content -LiteralPath $IndexPath -Raw -ErrorAction Stop
$index = $indexContent | ConvertFrom-Json -ErrorAction Stop

# --- Lecture de la matrice des modes (pour write_policy et write_policy) ---
$matrixPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json"
$matrix = @{ modes = @() }
if (Test-Path -LiteralPath $matrixPath) {
    $matrixContent = Get-Content -LiteralPath $matrixPath -Raw -ErrorAction SilentlyContinue
    if ($matrixContent) {
        $matrix = $matrixContent | ConvertFrom-Json -ErrorAction SilentlyContinue
    }
}

# --- Lecture du budget FREE ---
$budgetPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\free-budget.json"
$budget = @{ maxContextSizeBytes = 100000; maxRequestsPerSession = 50; currentRequestsCount = 0 }
if (Test-Path -LiteralPath $budgetPath) {
    $budgetContent = Get-Content -LiteralPath $budgetPath -Raw -ErrorAction SilentlyContinue
    if ($budgetContent) {
        $budget = $budgetContent | ConvertFrom-Json -ErrorAction SilentlyContinue
    }
}

# --- Récupérer write_policy du mode actif ---
$modeInfo = $matrix.modes | Where-Object { $_.mode_id -eq $ModeId } | Select-Object -First 1
$modeWritePolicy = if ($modeInfo) { $modeInfo.write_policy } else { "read_only" }
$modeKind = if ($modeInfo) { $modeInfo.kind } else { "rule_profile" }

# --- Normalisation de la demande ---
$requestLower = $Request.ToLower()

# --- Scoring par skill ---
$scoredSkills = @()

foreach ($s in $index.skills) {
    # Seuls les skills actifs sont routables
    if ($s.status -ne "active") { continue }

    $score = 0
    $matchedTriggers = @()
    $matchedAntiTriggers = @()

    # Scoring des triggers positifs
    foreach ($t in $s.triggers) {
        $tLower = $t.ToLower()
        if ($requestLower -match [regex]::Escape($tLower)) {
            $w = 3
            if ($s.weight -and $s.weight.Count -gt $matchedTriggers.Count) {
                $wVal = $s.weight[$matchedTriggers.Count]
                if ($wVal -match '^\d+$') { $w = [int]$wVal }
            }
            $score += $w
            $matchedTriggers += $t
        }
    }

    # Pénalité des anti_triggers
    foreach ($at in $s.anti_triggers) {
        $atLower = $at.ToLower()
        if ($requestLower -match [regex]::Escape($atLower)) {
            $score -= 5
            $matchedAntiTriggers += $at
        }
    }

    # --- T154 : Filtrer par mode actif (write_policy) ---
    $modeBlocked = $false
    if ($s.category -in @("cdp", "profil", "profile") -and $ModeId -eq "free") {
        # Les skills CDP ne sont pas accessibles en mode FREE (pas de port 9222)
        $modeBlocked = $true
        $warnings += "SKILL_EXCLU_MODE : $($s.name) exclu en mode FREE (accès CDP restreint)"
    }
    if ($modeWritePolicy -eq "read_only" -and $s.category -eq "execution") {
        $modeBlocked = $true
        $warnings += "SKILL_EXCLU_MODE : $($s.name) exclu en mode $ModeId (write_policy=read_only)"
    }

    # --- T155 : Vérifier budget FREE (contexte) ---
    if ($ModeId -eq "free" -and $ContextSize -gt 0) {
        $maxContext = $budget.maxContextSizeBytes
        if ($ContextSize -gt $maxContext) {
            $modeBlocked = $true
            $warnings += "SKILL_EXCLU_BUDGET : $($s.name) exclu - contexte $ContextSize octets dépasse le plafond $maxContext octets en mode FREE"
        }
        # Vérifier nombre de requêtes
        $currentReqs = $budget.currentRequestsCount
        if (($currentReqs + 1) -gt $budget.maxRequestsPerSession) {
            $modeBlocked = $true
            $warnings += "SKILL_EXCLU_BUDGET : $($s.name) exclu - nombre de requêtes dépasserait le maximum en mode FREE"
        }
    }

    if ($modeBlocked) {
        continue
    }

    if ($score -ge $MinScore -and $matchedAntiTriggers.Count -eq 0) {
        $scoredSkills += [PSCustomObject]@{
            name = $s.name
            version = $s.version
            category = $s.category
            score = $score
            base_score = $s.base_score
            matched_triggers = $matchedTriggers
            skill_path = $s.skill_path
            intent_hash = $s.intent_hash
            source_shard = $s.source_shard
            mode_compatible = $true
        }
    }
}

# --- Trier par score décroissant ---
$scoredSkills = $scoredSkills | Sort-Object score -Descending | Select-Object -First $MaxResults

# --- Journalisation de l'activation ---
$logDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs"
if (-not (Test-Path -LiteralPath $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
}
$logFile = Join-Path $logDir "skill-router.log"
$logLine = "[$nowUtc] MODE=$ModeId REQUEST='$Request' | MATCHES=$($scoredSkills.Count) | SKILLS=$($scoredSkills.name -join ', ')"
Add-Content -LiteralPath $logFile -Value $logLine -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "ROUTAGE DES SKILLS PAR MODE (T151 à T160)"
Write-Output "=============================================="
Write-Output "Mode actif   : $ModeId ($modeKind, write_policy=$modeWritePolicy)"
Write-Output "Demande      : $Request"
Write-Output "Index        : $IndexPath"
Write-Output "Skills actifs: $($index.active_skills)"
Write-Output "Matchs       : $($scoredSkills.Count)"
Write-Output "Score min    : $MinScore"
Write-Output "Max résultats: $MaxResults"
Write-Output "Contexte     : $ContextSize octets"
Write-Output "Horodatage   : $nowUtc"
Write-Output "=============================================="

if ($scoredSkills.Count -eq 0) {
    Write-Output "AUCUN SKILL ACTIVÉ — Aucun skill actif ne correspond à la demande dans le mode $ModeId."
    Write-Output "→ Candidate à distillation en fin de tâche (distill-skill.ps1)."
} else {
    foreach ($s in $scoredSkills) {
        Write-Output "ACTIVÉ : $($s.name) v$($s.version) | score=$($s.score) | catégorie=$($s.category)"
        Write-Output "  Chemin   : $($s.skill_path)"
        Write-Output "  Triggers : $($s.matched_triggers -join ', ')"
        Write-Output "  Intent   : $($s.intent_hash)"
        Write-Output "  Compatible mode $ModeId : Oui"
    }
}

if ($warnings.Count -gt 0) {
    Write-Output "=============================================="
    Write-Output "AVERTISSEMENTS :"
    foreach ($w in $warnings) { Write-Output "  - $w" }
}

Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    Write-Output "RESULTAT : ROUTAGE VALIDÉ"
    exit 0
}
