#!/usr/bin/env pwsh
# validate-skill.ps1 — Validation et promotion de skills (ENV3)
# Vérifie l'absence de doublon (name, intent_hash) avant promotion.
# Promeut un skill de draft à active avec incrément semver.
#
# Usage :
#   .\validate-skill.ps1 -BaseSkill <nom> -AutoPromote
#   .\validate-skill.ps1 -BaseSkill <nom> -NouvelleVersion <x.y.z>
#
# Après promotion, appelle index-skills.ps1 pour régénérer skills-index.json.

param (
    [Parameter(Mandatory = $true)]
    [string]$BaseSkill,

    [Parameter(Mandatory = $false)]
    [switch]$AutoPromote,

    [Parameter(Mandatory = $false)]
    [string]$NouvelleVersion
)

$ErrorActionPreference = "Stop"

$SKILLS_DIR = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
$SKILLS_INDEX = "$SKILLS_DIR\skills-index.json"
$SKILL_PATH = "$SKILLS_DIR\$BaseSkill"

if (-not (Test-Path -LiteralPath $SKILL_PATH)) {
    Write-Output "ERREUR: le skill $BaseSkill n'existe pas à $SKILL_PATH"
    exit 1
}

$SKILL_MD = "$SKILL_PATH\SKILL.md"
if (-not (Test-Path -LiteralPath $SKILL_MD)) {
    Write-Output "ERREUR: SKILL.md introuvable pour $BaseSkill"
    exit 1
}

# Lire le frontmatter YAML du SKILL.md
$contenu = Get-Content -LiteralPath $SKILL_MD -Raw
if ($contenu -notmatch '^---\s*$([\s\S]*?)^---\s*$') {
    Write-Output "ERREUR: frontmatter YAML manquant ou invalide dans $SKILL_MD"
    exit 1
}
$frontmatter = $Matches[1]

# Extraire les champs du frontmatter
function Get-YamlValeur($texte, $cle) {
    if ($texte -match ($cle + ':\s*(.+)')) {
        return $Matches[1].Trim().Trim('"')
    }
    return $null
}

$nomActuel = Get-YamlValeur $frontmatter 'name'
$intentHash = Get-YamlValeur $frontmatter 'intent_hash'
$statusActuel = Get-YamlValeur $frontmatter 'status'
$versionActuelle = Get-YamlValeur $frontmatter 'version'

if (-not $nomActuel) { $nomActuel = $BaseSkill }

# Vérifier l'absence de doublon dans skills-index.json
$raw = Get-Content -LiteralPath $SKILLS_INDEX -Raw
$index = $raw | ConvertFrom-Json
$skillsProps = $index.skills.PSObject.Properties

foreach ($prop in $skillsProps) {
    $s = $prop.Value
    $nomExist = $s.PSObject.Properties | Where-Object { $_.Name -eq 'name' } | Select-Object -First 1
    $ihExist = $s.PSObject.Properties | Where-Object { $_.Name -eq 'intent_hash' } | Select-Object -First 1
    if ($nomExist -and $nomExist.Value -eq $nomActuel) {
        Write-Output "ERREUR: doublon de nom détecté : $nomActuel existe déjà dans skills-index.json"
        exit 1
    }
    if ($ihExist -and $ihExist.Value -eq $intentHash) {
        Write-Output "ERREUR: doublon d'intent_hash détecté : $intentHash existe déjà dans skills-index.json"
        exit 1
    }
}

# Promotion draft -> active si AutoPromote
if ($AutoPromote) {
    if ($statusActuel -ne 'draft') {
        Write-Output "ERREUR: le skill $BaseSkill est en statut '$statusActuel', pas 'draft'. Promotion impossible."
        exit 1
    }

    # Calculer la nouvelle version
    if ($NouvelleVersion) {
        $nouvelleVersion = $NouvelleVersion
    }
    else {
        # Incrément patch : x.y.z -> x.y.(z+1)
        if ($versionActuelle -and $versionActuelle -match '^(\d+)\.(\d+)\.(\d+)$') {
            $maj = [int]$Matches[1]
            $mineur = [int]$Matches[2]
            $patch = [int]$Matches[3] + 1
            $nouvelleVersion = "$maj.$mineur.$patch"
        }
        else {
            $nouvelleVersion = "0.1.1"
        }
    }

    # Mettre à jour le frontmatter (status: active, version)
    $nouveauFrontmatter = $frontmatter
    $nouveauFrontmatter = $nouveauFrontmatter -replace '^status:\s*.+$', "status: active" -replace '^version:\s*.+$', "version: $nouvelleVersion"
    
    # Reconstituer le fichier
    $corps = $contenu -replace '^---\s*$[\s\S]*?^---\s*$', ''
    $nouveauContenu = "--`n" + $nouveauFrontmatter + "`n--`n" + $corps
    Set-Content -LiteralPath $SKILL_MD -Value $nouveauContenu -Encoding UTF8

    Write-Output ("PROMOTION: $BaseSkill promu de draft à active, version " + $nouvelleVersion)
    $statusFinal = 'active'
    $versionFinale = $nouvelleVersion
}
else {
    Write-Output ("VALIDATION: $BaseSkill verifie (statut: " + $statusActuel + ", version: " + $versionActuelle + ")")
    $statusFinal = $statusActuel
    $versionFinale = $versionActuelle
}

# Appeler index-skills.ps1 pour régénérer l'index
$INDEX_SCRIPT = "$SKILLS_DIR\index-skills.ps1"
if (Test-Path -LiteralPath $INDEX_SCRIPT) {
    & $INDEX_SCRIPT
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ATTENTION: index-skills.ps1 a retourné un code d'erreur"
    }
}
else {
    Write-Output "ATTENTION: index-skills.ps1 introuvable, l'index n'a pas été régénéré"
}

exit 0
