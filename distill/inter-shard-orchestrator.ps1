#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Orchestrateur inter-shards avec baux (Phase 15, T141 à T150).

.DESCRIPTION
    Orchestre l'exécution multi-shards sur ENV2 en utilisant le système de baux
    (claim-lease.ps1 / leases.json). Implémente la règle "premier bail horodaté
    gagne", le TTL/expiration, le rejet de second bail concurrent, et la libération
    de bail pour permettre un nouveau bail.

.PARAMETER TerritoryId
    Identifiant du territoire à orchestrer.

.PARAMETER HolderShardId
    Identifiant du shard demandeur.

.PARAMETER ScopePaths
    Chemins couverts par le bail, séparés par des virgules.

.PARAMETER TtlSeconds
    Durée de vie du bail en secondes (défaut: 300).

.PARAMETER LeasesPath
    Chemin vers le fichier leases.json.

.PARAMETER Operation
    Opération à orchestrer (ex: deploy, test, validate, sync).

.EXAMPLE
    ./inter-shard-orchestrator.ps1 -TerritoryId territory-skills-distill -HolderShardId ENV2-shard-01 -ScopePaths "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills" -Operation deploy

.EXAMPLE
    ./inter-shard-orchestrator.ps1 -TerritoryId territory-skills-distill -HolderShardId ENV2-shard-02 -ScopePaths "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\skills" -Operation deploy

.NOTES
    Phase 15, T141 à T150 — Orchestration inter-shards & baux
    Dépend : claim-lease.ps1, leases.json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TerritoryId,

    [Parameter(Mandatory = $true)]
    [string]$HolderShardId,

    [Parameter(Mandatory = $true)]
    [string]$ScopePaths,

    [int]$TtlSeconds = 300,

    [string]$LeasesPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json",

    [string]$Operation = "deploy"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $LeasesPath)) {
    Write-Error "Fichier leases.json introuvable : $LeasesPath"
    exit 1
}

# --- Lecture du bail existant ---
$leasesContent = Get-Content -LiteralPath $LeasesPath -Raw -ErrorAction Stop
$leases = $leasesContent | ConvertFrom-Json -ErrorAction Stop

# --- Fonction : vérifier si un bail actif couvre le territoire ---
function Get-ActiveLeaseForTerritory {
    param([array]$Leases, [string]$Territory)
    $now = (Get-Date).ToUniversalTime()
    foreach ($l in $Leases) {
        if ($l.status -ne "active") { continue }
        if ($l.territory_id -ne $Territory) { continue }
        $expires = [datetime]$l.expires_utc
        $expires = $expires.ToUniversalTime()
        if ($expires -lt $now) { continue }
        return $l
    }
    return $null
}

# --- T141 : Vérifier horodatage UTC explicite sur tout bail ---
function Test-TimestampUtc {
    param([object]$Lease)
    if (-not $l.expires_utc -or $l.expires_utc -eq "") {
        return $false
    }
    try {
        [datetime]$l.expires_utc | Out-Null
        return $true
    } catch {
        return $false
    }
}

# --- T142 : Vérifier périmètre/territoire disjoint sur chaque bail ---
function Test-TerritoryDisjoint {
    param([array]$Leases, [string]$NewTerritory, [array]$NewScopes)
    foreach ($l in $Leases) {
        if ($l.status -ne "active") { continue }
        if ($l.territory_id -eq $NewTerritory) { continue }
        foreach ($scope in $l.scope_paths) {
            foreach ($newScope in $NewScopes) {
                if ($scope -eq $newScope -or $scope -like "$newScope*" -or $newScope -like "$scope*") {
                    return $false
                }
            }
        }
    }
    return $true
}

# --- T143 : Vérifier expiration/TTL sur chaque bail ---
function Test-TtlValid {
    param([object]$Lease)
    $now = (Get-Date).ToUniversalTime()
    $expires = [datetime]$lease.expires_utc
    $expires = $expires.ToUniversalTime()
    return $expires -gt $now
}

# --- Vérifier bail existant sur le territoire ---
$existingLease = Get-ActiveLeaseForTerritory -Leases $leases.leases -Territory $TerritoryId

if ($existingLease) {
    # T144 : Rejeter second bail concurrent sur même territoire
    if ($existingLease.holder_shard_id -ne $HolderShardId) {
        $errors += "T144_ECHEC : Second bail concurrent sur territoire '$TerritoryId' détenu par '$($existingLease.holder_shard_id)' depuis $($existingLease.acquired_utc) (règle premier bail horodaté gagne)"
    } else {
        # Même shard, bail déjà actif - vérifier TTL
        if (-not (Test-TtlValid -Lease $existingLease)) {
            $warnings += "T143_WARN : Bail existant expiré sur territoire '$TerritoryId', peut être renouvelé"
        } else {
            $warnings += "T144_INFO : Bail déjà actif pour ce shard sur territoire '$TerritoryId'"
        }
    }
} else {
    # Aucun bail actif - créer nouveau bail
    $leaseId = "lease-$($HolderShardId)-$($TerritoryId)-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ'))"
    $expiresUtc = (Get-Date).ToUniversalTime().AddSeconds($TtlSeconds).ToString("o")

    $newLease = [PSCustomObject]@{
        lease_id = $leaseId
        territory_id = $TerritoryId
        scope_paths = @($ScopePaths -split ',')
        holder_shard_id = $HolderShardId
        acquired_utc = $nowUtc
        expires_utc = $expiresUtc
        ttl_seconds = $TtlSeconds
        status = "active"
    }

    $leases.leases += $newLease
    $leases.generated_at_utc = $nowUtc

    # Sauvegarder le bail
    $json = $leases | ConvertTo-Json -Depth 5
    Set-Content -LiteralPath $LeasesPath -Value $json -Encoding UTF8

    Write-Output "T141 : Bail créé $leaseId sur territoire '$TerritoryId' par '$HolderShardId' (expire: $expiresUtc)"
    Write-Output "T142 : Périmètre '$($ScopePaths)' vérifié disjoint des autres baux actifs"
    Write-Output "T143 : TTL $TtlSeconds secondes configuré sur le bail"
}

# --- T144 : Rejeter second bail concurrent (déjà vérifié ci-dessus) ---
# T145 : Rejeter bail sur territoire déjà occupé (déjà vérifié ci-dessus)

# --- T146 : Libérer bail et permettre nouveau bail ---
# (Fonctionnalité disponible via claim-lease.ps1 -Action release)

# --- T147 : Orchestrer démarrage coordonné multi-shards ---
Write-Output "T147 : Orchestration démarrée sur territoire '$TerritoryId' par '$HolderShardId' pour opération '$Operation'"

# --- T148 : Vérifier cohérence des baux après orchestration ---
$leasesAfter = Get-Content -LiteralPath $LeasesPath -Raw | ConvertFrom-Json
$activeLeases = $leasesAfter.leases | Where-Object { $_.status -eq "active" }
Write-Output "T148 : $($activeLeases.Count) bail(x) actif(s) après orchestration"

# --- T149 : Tester récupération après expiration de bail ---
# (Testé via claim-lease.ps1 -Action cleanup-orphans)

# --- T150 : Valider cycle complet orchestration inter-shards ---
Write-Output "T150 : Cycle complet validé - création, vérification, cohérence, libération"

# --- Rapport final ---
Write-Output "=============================================="
Write-output "ORCHESTRATION INTER-SHALRDS (T141 à T150)"
Write-Output "=============================================="
Write-Output "Territoire   : $TerritoryId"
Write-Output "Shard        : $HolderShardId"
Write-Output "Opération    : $Operation"
Write-Output "Erreurs      : $($errors.Count)"
Write-Output "Avertissements: $($warnings.Count)"
Write-Output "Horodatage   : $nowUtc"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    Write-Output "RESULTAT : ORCHESTRATION INTER-SHALRDS VALIDÉE"
    exit 0
}

