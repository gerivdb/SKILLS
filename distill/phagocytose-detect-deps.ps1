#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Détection des dépendances non adaptées à ENV2 (Z600, pas d'AVX2, RAM 24 Go).

.DESCRIPTION
    Analyse un fichier source (script Python, PowerShell, Zig, etc.) pour détecter
    les dépendances qui peuvent ne pas être adaptées à l'environnement ENV2 :
    - Bibliothèques nécessitant AVX2/AVX-512 (incompatible avec Xeon E5620)
    - Outils gourmands en RAM (> 8 Go)
    - Dépendances exotiques non disponibles sur ENV2

    Conforme à PHAGOCYTOSE-SPEC.md (T038).

.PARAMETER SourcePath
    Chemin vers le fichier source à analyser.

.PARAMETER SkillName
    Nom du skill associé (pour le rapport).

.PARAMETER ReportPath
    Chemin du fichier de rapport de détection (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\reports\<skill>-deps-<timestamp>.json).

.EXAMPLE
    ./phagocytose-detect-deps.ps1 -SourcePath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\distill-skill.ps1" -SkillName "distill-skill"

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md (Phase 4, T038)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath,

    [string]$SkillName,

    [string]$ReportPath
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution du chemin (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $SourcePath)) {
    Write-Error "Source introuvable : $SourcePath"
    exit 1
}

if (-not $SkillName) {
    $SkillName = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
}

if (-not $ReportPath) {
    $reportDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\reports"
    if (-not (Test-Path -LiteralPath $reportDir)) {
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
    }
    $ReportPath = Join-Path $reportDir "$($SkillName)-deps-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ')).json"
}

# --- ENV2 Hardware Constraints ---
$env2Constraints = [PSCustomObject]@{
    cpu = "2x Intel Xeon E5620 (Westmere-EP, SSE4.2 max, pas d'AVX2)"
    ram_total_gb = 24
    ram_recommandee_max_gb = 8
    architecture = "x86_64 dual-socket ~2010-2011"
    avx2 = $false
    avx512 = $false
}

# --- Détection des dépendances problématiques ---
$sourceContent = Get-Content -LiteralPath $SourcePath -Raw -ErrorAction Stop
$lignes = $sourceContent -split "`n"

$depsProblemes = @()

foreach ($ligne in $lignes) {
    $trimmed = $ligne.Trim()

    # Détection imports/bibliothèques lourdes ou AVX2-dépendantes
    if ($trimmed -match '(?i)(numpy|scipy|pandas|tensorflow|torch|pytorch|cv2|opencv|scikit-learn|sklearn)') {
        $depsProblemes += [PSCustomObject]@{
            ligne = $trimmed
            type = "bibliothèque_lourde"
            risque = "AVX2 ou RAM élevée requise, incompatible ENV2 (Xeon E5620, pas d'AVX2)"
            recommandation = "Vérifier une alternative légère ou pur-python"
        }
    }
    # Détection imports de cryptographie lourde
    elseif ($trimmed -match '(?i)(cryptography|pycryptodome|bcrypt|scrypt|argon2)') {
        $depsProblemes += [PSCustomObject]@{
            ligne = $trimmed
            type = "crypto_lourde"
            risque = "Peut nécessiter des instructions CPU non disponibles sur ENV2"
            recommandation = "Tester sur ENV2 avant promotion"
        }
    }
    # Détection de requêtes réseau directes (interdites en BDCP)
    elseif ($trimmed -match '(?i)(urllib|requests|http.client|axios|fetch|curl|wget)') {
        $depsProblemes += [PSCustomObject]@{
            ligne = $trimmed
            type = "reseau_direct"
            risque = "Interdit en mode BDCP (clapet fermé), doit passer par CDP port 9222"
            recommandation = "Remplacer par un appel CDP ou protocole local"
        }
    }
    # Détection de chemins relatifs ambigus
    elseif ($trimmed -match '(?i)(\.\./|~\/|\$env:HOME|\$USERPROFILE)') {
        $depsProblemes += [PSCustomObject]@{
            ligne = $trimmed
            type = "chemin_ambigu"
            risque = "Chemin relatif ou dépendant de l'environnement, risque de dérive"
            recommandation = "Utiliser un chemin absolu explicite (règle explicit-path-compliance)"
        }
    }
    # Détection de consommation mémoire élevée
    elseif ($trimmed -match '(?i)(read_all|read_text|load_all|open\(.*\.read\(\)|slurp)') {
        $depsProblemes += [PSCustomObject]@{
            ligne = $trimmed
            type = "memoire_élevée"
            risque = "Peut charger un fichier entier en mémoire, risqué sur 24 Go DDR3"
            recommandation = "Utiliser la lecture par chunks ou streaming"
        }
    }
}

# --- Construction du rapport ---
$rapport = [PSCustomObject]@{
    date_utc = $nowUtc
    source = $SourcePath
    skill = $SkillName
    env2 = $env2Constraints
    dependances_problemes = @($depsProblemes)
    nb_problemes = $depsProblemes.Count
    verdict = if ($depsProblemes.Count -eq 0) { "ADAPTE_ENV2" } else { "NON_ADAPTE_ENV2" }
}

$rapportJson = $rapport | ConvertTo-Json -Depth 4
Set-Content -LiteralPath $ReportPath -Value $rapportJson -Encoding UTF8

# --- Rapport console ---
Write-Output "=============================================="
Write-output "DÉTECTION DÉPENDANCES ENV2 (T038)"
Write-Output "=============================================="
Write-Output "Source        : $SourcePath"
Write-Output "Skill         : $SkillName"
Write-Output "Rapport       : $ReportPath"
Write-Output "Problèmes     : $($depsProblemes.Count)"
Write-Output "Verdict       : $($rapport.verdict)"
Write-Output "=============================================="

if ($depsProblemes.Count -gt 0) {
    Write-Output "DÉPENDANCES PROBLÈMES :"
    foreach ($d in $depsProblemes) {
        Write-Output "  - $($d.type) : $($d.ligne)"
        Write-Output "    Risque   : $($d.risque)"
        Write-Output "    Recommandation : $($d.recommandation)"
    }
    Write-Output "=============================================="
    Write-Output "VERDICT : NON ADAPTÉ ENV2 — Corriger avant promotion du skill."
    exit 1
} else {
    Write-Output "VERDICT : ADAPTÉ ENV2 — Aucun problème détecté."
}

Write-Output "=============================================="
