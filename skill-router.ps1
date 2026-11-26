#!/usr/bin/env pwsh
# skill-router.ps1 — Routeur de skills pour Kilo Code (ENV3)
# Consulte D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json pour matcher
# une tâche à un skill canonique (par nom, trigger ou intent_hash).
#
# Usage :
#   .\skill-router.ps1 -Nom <nom_skill>
#   .\skill-router.ps1 -Trigger <mot_cle>
#   .\skill-router.ps1 -IntentHash <0x...>
#
# Retourne JSON sur stdout : nom, status, path, triggers, intent_hash, source_repo, layer
# Exit code 0 si skill trouvé et actif, 1 sinon.

param (
    [Parameter(Mandatory = $false)]
    [string]$Nom,

    [Parameter(Mandatory = $false)]
    [string]$Trigger,

    [Parameter(Mandatory = $false)]
    [string]$IntentHash
)

$ErrorActionPreference = "Stop"

$SKILLS_INDEX = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json"

if (-not (Test-Path -LiteralPath $SKILLS_INDEX)) {
    Write-Output "ERREUR: skills-index.json introuvable: $SKILLS_INDEX"
    exit 1
}

$raw = Get-Content -LiteralPath $SKILLS_INDEX -Raw
$index = $raw | ConvertFrom-Json

if (-not $index.PSObject.Properties.Name -contains 'skills') {
    Write-Output "ERREUR: skills-index.json ne contient pas de propriete 'skills'"
    exit 1
}

$skillsProps = $index.skills.PSObject.Properties

# Déterminer le critère de recherche
$cleRecherche = $null
$valeurRecherche = $null
if ($PSBoundParameters.ContainsKey('Nom')) {
    $cleRecherche = 'nom_cle'
    $valeurRecherche = $Nom
}
elseif ($PSBoundParameters.ContainsKey('Trigger')) {
    $cleRecherche = 'trigger'
    $valeurRecherche = $Trigger
}
elseif ($PSBoundParameters.ContainsKey('IntentHash')) {
    $cleRecherche = 'intent_hash'
    $valeurRecherche = $IntentHash
}
else {
    Write-Output "ERREUR: un critère est requis (-Nom, -Trigger ou -IntentHash)"
    exit 1
}

# Rechercher le skill parmi les propriétés du registre
$resultat = $null
$nomSkillTrouve = $null
foreach ($prop in $skillsProps) {
    $nomSkill = $prop.Name
    $s = $prop.Value

    if ($cleRecherche -eq 'nom_cle') {
        # Le nom est la clé du dictionnaire
        if ($nomSkill -eq $valeurRecherche) {
            $resultat = $s
            $nomSkillTrouve = $nomSkill
            break
        }
    }
    else {
        # Trigger et intent_hash sont des propriétés à l'intérieur
        $propRecherchee = $s.PSObject.Properties | Where-Object { $_.Name -eq $cleRecherche }
        if ($propRecherchee -and $propRecherchee.Value -eq $valeurRecherche) {
            $resultat = $s
            $nomSkillTrouve = $nomSkill
            break
        }
    }
}

if (-not $resultat) {
    Write-Output ("ERREUR: aucun skill correspondant trouvé (" + $cleRecherche + " = " + $valeurRecherche + ")")
    exit 1
}

if ($resultat.status -ne 'active') {
    Write-Output ("ATTENTION: le skill " + $nomSkillTrouve + " existe mais son statut est '" + $resultat.status + "', pas 'active'")
    exit 1
}

# Construire la sortie
$sortie = [ordered]@{}
$sortie['nom'] = $nomSkillTrouve
$sortie['status'] = $resultat.status
if ($resultat.PSObject.Properties.Name -contains 'path') { $sortie['path'] = $resultat.path }
if ($resultat.PSObject.Properties.Name -contains 'triggers') { $sortie['triggers'] = $resultat.triggers }
if ($resultat.PSObject.Properties.Name -contains 'intent_hash') { $sortie['intent_hash'] = $resultat.intent_hash }
if ($resultat.PSObject.Properties.Name -contains 'source_repo') { $sortie['source_repo'] = $resultat.source_repo }
if ($resultat.PSObject.Properties.Name -contains 'layer') { $sortie['layer'] = $resultat.layer }

$sortie | ConvertTo-Json -Depth 3
exit 0
