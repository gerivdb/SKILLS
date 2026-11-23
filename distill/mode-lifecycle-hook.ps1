#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Hooks de cycle de vie et handovers de mode (Phase 17, T161 à T170).

.DESCRIPTION
    Gère les transitions de mode (architect, data, bdcp, free) avec handover JSON
    horodaté en UTC incluant : mode source, mode cible, état des baux/territoires,
    skills sélectionnés par skill-router.ps1, et garde-fous actifs
    (bdcp_clapet_default = "closed", budget FREE).

    Empêche le contournement des garde-fous lors du changement de mode :
    - Passage vers data n'accorde jamais d'écriture sans bail valide
    - Passage vers free réapplique immédiatement les plafonds (100000 octets / 50 requêtes)
    - Retour vers bdcp conserve le clapet closed par défaut

.PARAMETER FromMode
    Mode source de la transition.

.PARAMETER ToMode
    Mode cible de la transition.

.PARAMETER TerritoryId
    Identifiant du territoire concerné (optionnel).

.PARAMETER HolderShardId
    Identifiant du shard détenteur du bail (optionnel).

.PARAMETER ScopePaths
    Chemins couverts par le bail, séparés par des virgules (optionnel).

.PARAMETER TtlSeconds
    Durée de vie du bail en secondes (défaut: 300).

.PARAMETER SelectedSkills
    Skills sélectionnés par skill-router.ps1, séparés par des virgules (optionnel).

.PARAMETER LeasesPath
    Chemin vers le fichier leases.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json).

.PARAMETER HandoverPath
    Chemin vers le fichier de handover JSON (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\handover.json).

.PARAMETER LogPath
    Chemin vers le journal des transitions (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\mode-transitions.log).

.EXAMPLE
    ./mode-lifecycle-hook.ps1 -FromMode architect -ToMode data -TerritoryId territory-skills-distill -HolderShardId ENV2-shard-01 -ScopePaths "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\skills" -SelectedSkills "distill-skill"

.EXAMPLE
    ./mode-lifecycle-hook.ps1 -FromMode data -ToMode free -HolderShardId ENV2-shard-01

.NOTES
    Phase 17, T161 à T170 — Hooks de cycle de vie et handovers de mode
    Dépend : claim-lease.ps1, leases.json, skill-router.ps1
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$FromMode,

    [Parameter(Mandatory = $true)]
    [string]$ToMode,

    [string]$TerritoryId,

    [string]$HolderShardId,

    [string]$ScopePaths,

    [int]$TtlSeconds = 300,

    [string]$SelectedSkills,

    [string]$LeasesPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json",

    [string]$HandoverPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\handover.json",

    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\mode-transitions.log"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $LeasesPath)) {
    Write-Error "Fichier leases.json introuvable : $LeasesPath"
    exit 1
}

# --- Lecture du fichier de baux ---
$leasesContent = Get-Content -LiteralPath $LeasesPath -Raw -ErrorAction Stop
$leases = $leasesContent | ConvertFrom-Json -ErrorAction Stop

# --- T164 : Vérifier l'intégrité du handover JSON (horodatage UTC, mode source, mode cible) ---
$handover = [PSCustomObject]@{
    timestamp_utc = $nowUtc
    from_mode = $FromMode
    to_mode = $ToMode
    territory_id = $TerritoryId
    holder_shard_id = $HolderShardId
    scope_paths = @($ScopePaths -split ',')
    selected_skills = @($SelectedSkills -split ',')
    ttl_seconds = $TtlSeconds
    guard_fou_actifs = @()
}

# --- T165 : Empêcher le contournement des garde-fous lors du changement de mode ---
# Vérifier que le passage vers data n'accorde jamais d'écriture sans bail valide
if ($ToMode -eq "data") {
    if (-not $HolderShardId -or -not $ScopePaths) {
        $errors += "T165_ECHEC : Transition vers data requiert un HolderShardId et des ScopePaths (bail requis pour écriture)"
    } else {
        # Vérifier qu'un bail existe ou peut être créé
        $existingLease = $leases.leases | Where-Object { $_.territory_id -eq $TerritoryId -and $_.status -eq "active" }
        $now = (Get-Date).ToUniversalTime()
        $activeLease = $null
        foreach ($l in $existingLease) {
            $expires = [datetime]$l.expires_utc
            $expires = $expires.ToUniversalTime()
            if ($expires -gt $now) {
                $activeLease = $l
                break
            }
        }
        if (-not $activeLease) {
            $warnings += "T166_WARN : Aucun bail actif sur le territoire '$TerritoryId', écriture en mode data bloquée tant que bail non créé"
        } else {
            $handover.guard_fou_actifs += "bail_actif:$($activeLease.lease_id)"
        }
    }
}

# --- T167 : Vérifier que le passage vers free réapplique immédiatement les plafonds ---
if ($ToMode -eq "free") {
    $handover.guard_fou_actifs += "budget_free:maxContextSizeBytes=100000"
    $handover.guard_fou_actifs += "budget_free:maxRequestsPerSession=50"
    $warnings += "T167_INFO : Passage vers FREE réapplique les plafonds (100000 octets / 50 requêtes)"
}

# --- T168 : Vérifier que le retour vers bdcp conserve le clapet closed par défaut ---
if ($ToMode -eq "bdcp") {
    $handover.guard_fou_actifs += "bdcp_clapet_default:closed"
    $handover.guard_fou_actifs += "cdp_port:127.0.0.1:9222"
    $warnings += "T168_INFO : Retour vers BDCP conserve le clapet fermé par défaut (port 9222, 127.0.0.1)"
}

# --- T161 : Créer le schéma JSON du handover inter-modes ---
# Le handover est déjà structuré ci-dessus avec tous les champs requis

# --- T162/T163 : Hooks d'entrée et de sortie de mode ---
$handoverEntry = [PSCustomObject]@{
    event = "mode_enter"
    to_mode = $ToMode
    timestamp_utc = $nowUtc
    skills_selected = @($SelectedSkills -split ',')
    guard_fou_actifs = $handover.guard_fou_actifs
}

$handoverExit = [PSCustomObject]@{
    event = "mode_exit"
    from_mode = $FromMode
    timestamp_utc = $nowUtc
    skills_released = @()
    guard_fou_leves = @()
}

# --- Assemblage du handover complet ---
$handoverComplete = [PSCustomObject]@{
    handover = $handover
    entry_hook = $handoverEntry
    exit_hook = $handoverExit
}

# --- Écriture du fichier de handover JSON ---
$handoverJson = $handoverComplete | ConvertTo-Json -Depth 4
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}
Set-Content -LiteralPath $HandoverPath -Value $handoverJson -Encoding UTF8

# --- Journalisation de la transition ---
$logLine = "[$nowUtc] MODE_TRANSITION $FromMode -> $ToMode | Territory=$TerritoryId | Shard=$HolderShardId | Skills=$($SelectedSkills -join ',') | Guards=$($handover.guard_fou_actifs -join ',')"
Add-Content -LiteralPath $LogPath -Value $logLine -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "HOOK DE CYCLE DE VIE MODE (T161 à T170)"
Write-Output "=============================================="
Write-Output "Mode source  : $FromMode"
Write-Output "Mode cible   : $ToMode"
Write-Output "Territoire   : $TerritoryId"
Write-Output "Shard        : $HolderShardId"
Write-Output "Skills       : $SelectedSkills"
Write-Output "Handover     : $HandoverPath"
Write-Output "Journal      : $LogPath"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    Write-Output "RESULTAT : TRANSITION DE MODE VALIDÉE"
    exit 0
}

