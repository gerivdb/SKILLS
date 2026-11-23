#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gestion des baux d'exclusion swarm sur ENV2 (inspiré Antigravity).

.DESCRIPTION
    Permet de revendiquer, renouveler, libérer et vérifier des baux sur des
    territoires inter-shards. Implémente la règle "premier bail horodaté gagne",
    le TTL avec expiration automatique, le garde-fou pré-écriture, et la
    journalisation des conflits.

    Conformément à SPEC-SKILL-FORMAT.md et à la règle de gouvernance
    kilo-modes-bdcp-free.md (Phase 2).

.PARAMETER Action
    Action à effectuer : claim, renew, release, check, list, cleanup-orphans.

.PARAMETER LeaseId
    Identifiant du bail (requis pour claim, renew, release, check).

.PARAMETER TerritoryId
    Identifiant du territoire (requis pour claim).

.PARAMETER HolderShardId
    Identifiant du shard détenteur (requis pour claim).

.PARAMETER ScopePaths
    Chemins couverts par le bail, séparés par des virgules (requis pour claim).

.PARAMETER TtlSeconds
    Durée de vie du bail en secondes (défaut: 300).

.PARAMETER LeasesPath
    Chemin vers le fichier leases.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json).

.EXAMPLE
    ./claim-lease.ps1 -Action claim -TerritoryId territory-skills-distill -HolderShardId ENV2-shard-01 -ScopePaths "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills" -TtlSeconds 300

.EXAMPLE
    ./claim-lease.ps1 -Action check -LeaseId lease-ENV2-skills-001

.EXAMPLE
    ./claim-lease.ps1 -Action release -LeaseId lease-ENV2-skills-001

.NOTES
    Intégration: kilo-modes-bdcp-free.md (Phase 2, T018-T020)
    Schéma: leases.schema.json (T021)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("claim", "renew", "release", "check", "list", "cleanup-orphans")]
    [string]$Action,

    [string]$LeaseId,

    [string]$TerritoryId,

    [string]$HolderShardId,

    [string]$ScopePaths,

    [int]$TtlSeconds = 300,

    [string]$LeasesPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime()

# --- Vérification pré-exécution du chemin (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $LeasesPath)) {
    Write-Error "Fichier de registre de baux introuvable : $LeasesPath"
    exit 1
}

# --- Lecture du registre ---
$leasesContent = Get-Content -LiteralPath $LeasesPath -Raw -ErrorAction Stop
$leases = $leasesContent | ConvertFrom-Json -ErrorAction Stop

function Save-Leases {
    param([object]$Data)
    $json = $Data | ConvertTo-Json -Depth 5
    Set-Content -LiteralPath $LeasesPath -Value $json -Encoding UTF8
}

function Get-LeaseById {
    param([string]$Id)
    $leases.leases | Where-Object { $_.lease_id -eq $Id } | Select-Object -First 1
}

function Get-ActiveLeaseForTerritory {
    param([string]$Territory)
    $leases.leases | Where-Object { $_.territory_id -eq $Territory -and $_.status -eq "active" } | Sort-Object acquired_utc | Select-Object -First 1
}

function Is-LeaseExpired {
    param([object]$Lease)
    $expires = [datetime]$Lease.expires_utc
    $expires = $expires.ToUniversalTime()
    return $expires -lt $nowUtc
}

# --- Journalisation des conflits ---
$conflictLogPath = Join-Path (Split-Path -Parent $LeasesPath) "lease-conflicts.log"
function Write-ConflictLog {
    param([string]$Message)
    $line = "[$nowUtc] $Message"
    Add-Content -LiteralPath $conflictLogPath -Value $line -Encoding UTF8
}

# --- Action : claim (revendiquer un bail) ---
if ($Action -eq "claim") {
    if (-not $TerritoryId) { Write-Error "TerritoryId requis pour claim"; exit 1 }
    if (-not $HolderShardId) { Write-Error "HolderShardId requis pour claim"; exit 1 }
    if (-not $ScopePaths) { Write-Error "ScopePaths requis pour claim"; exit 1 }

    # Vérifier s'il existe déjà un bail actif sur ce territoire
    $existing = Get-ActiveLeaseForTerritory -Territory $TerritoryId

    if ($existing) {
        # Règle premier bail horodaté gagne
        $existingAcquired = [datetime]$existing.acquired_utc
        $existingAcquired = $existingAcquired.ToUniversalTime()

        # Le nouveau bail ne peut pas l'emporter si l'existant est encore valide
        if (-not (Is-LeaseExpired -Lease $existing)) {
            $errors += "BAIL_OCCUPE: Le territoire '$TerritoryId' est détenu par '$($existing.holder_shard_id)' depuis $($existing.acquired_utc) (règle premier bail horodaté gagne)."
            Write-ConflictLog "CONFLIT claim '$TerritoryId' par '$HolderShardId' rejeté — détenteur actuel: '$($existing.holder_shard_id)' depuis $($existing.acquired_utc)"
        } else {
            # Bail expiré, peut être repris
            $warnings += "BAIL_EXPIRE: Le bail précédent sur '$TerritoryId' est expiré, reprise autorisée."
        }
    }

    if ($errors.Count -eq 0) {
        $leaseId = $LeaseId
        if (-not $leaseId) {
            $leaseId = "lease-$($HolderShardId)-$($TerritoryId)-$($nowUtc.ToString('yyyyMMddTHHmmss'))"
        }

        $expiresUtc = $nowUtc.AddSeconds($TtlSeconds).ToString("o")

        $newLease = [PSCustomObject]@{
            lease_id = $leaseId
            territory_id = $TerritoryId
            scope_paths = @($ScopePaths -split ',')
            holder_shard_id = $HolderShardId
            acquired_utc = $nowUtc.ToString("o")
            expires_utc = $expiresUtc
            ttl_seconds = $TtlSeconds
            status = "active"
        }

        $leases.leases += $newLease
        $leases.generated_at_utc = $nowUtc.ToString("o")
        Save-Leases -Data $leases

        Write-Output "BAIL_ACQUIS: $leaseId sur territoire '$TerritoryId' par '$HolderShardId' (expire: $expiresUtc)"
    }
}

# --- Action : renew (renouveler un bail) ---
elseif ($Action -eq "renew") {
    if (-not $LeaseId) { Write-Error "LeaseId requis pour renew"; exit 1 }

    $lease = Get-LeaseById -Id $LeaseId
    if (-not $lease) {
        Write-Error "Le bail '$LeaseId' n'existe pas."
        exit 1
    }

    if ($lease.status -ne "active") {
        Write-Error "Le bail '$LeaseId' n'est pas actif (statut: $($lease.status))."
        exit 1
    }

    if (Is-LeaseExpired -Lease $lease) {
        $warnings += "BAIL_EXPIRE: Le bail '$LeaseId' est expiré. Renouvellement refusé, créez un nouveau bail."
    } else {
        $newExpires = $nowUtc.AddSeconds($lease.ttl_seconds).ToString("o")
        $lease.expires_utc = $newExpires
        $leases.generated_at_utc = $nowUtc.ToString("o")
        Save-Leases -Data $leases
        Write-Output "BAIL_RENOUVLE: $leaseId (nouvelle expiration: $newExpires)"
    }
}

# --- Action : release (libérer un bail) ---
elseif ($Action -eq "release") {
    if (-not $LeaseId) { Write-Error "LeaseId requis pour release"; exit 1 }

    $lease = Get-LeaseById -Id $LeaseId
    if (-not $lease) {
        Write-Error "Le bail '$LeaseId' n'existe pas."
        exit 1
    }

    if ($lease.status -ne "active") {
        $warnings += "Le bail '$LeaseId' n'est pas actif (statut: $($lease.status))."
    } else {
        $lease.status = "released"
        $leases.generated_at_utc = $nowUtc.ToString("o")
        Save-Leases -Data $leases
        Write-Output "BAIL_LIBERE: $leaseId"
    }
}

# --- Action : check (vérifier un bail) ---
elseif ($Action -eq "check") {
    if (-not $LeaseId) { Write-Error "LeaseId requis pour check"; exit 1 }

    $lease = Get-LeaseById -Id $LeaseId
    if (-not $lease) {
        Write-Error "Le bail '$LeaseId' n'existe pas."
        exit 1
    }

    $expired = Is-LeaseExpired -Lease $lease
    $status = $lease.status
    if ($expired -and $status -eq "active") {
        $status = "expired (TTL dépassé)"
        $warnings += "Le bail '$LeaseId' est expiré mais pas encore marqué comme tel."
    }

    Write-Output "BAIL_VERIFIE: $leaseId"
    Write-Output "  Territoire : $($lease.territory_id)"
    Write-Output "  Détenteur  : $($lease.holder_shard_id)"
    Write-Output "  Statut     : $status"
    Write-Output "  Acquis     : $($lease.acquired_utc)"
    Write-Output "  Expire     : $($lease.expires_utc)"
    Write-Output "  TTL        : $($lease.ttl_seconds)s"
    Write-Output "  Chemins    : $($lease.scope_paths -join ', ')"
}

# --- Action : list (lister tous les baux) ---
elseif ($Action -eq "list") {
    Write-Output "REGISTRE DES BAX ($($leases.leases.Count) bail(s))"
    Write-Output "=============================================="
    foreach ($l in $leases.leases) {
        $expired = Is-LeaseExpired -Lease $l
        $status = $l.status
        if ($expired -and $status -eq "active") { $status = "expired (TTL dépassé)" }
        Write-Output "  $($l.lease_id) | $($l.territory_id) | $($l.holder_shard_id) | $status | expire: $($l.expires_utc)"
    }
}

# --- Action : cleanup-orphans (résoudre baux orphelins) ---
elseif ($Action -eq "cleanup-orphans") {
    $cleaned = 0
    foreach ($l in $leases.leases) {
        if ($l.status -eq "active" -and (Is-LeaseExpired -Lease $l)) {
            $l.status = "expired"
            $cleaned++
            Write-Output "BAIL_EXPIRE_ORPHELIN: $($l.lease_id) (territoire: $($l.territory_id), détenteur: $($l.holder_shard_id))"
        }
    }
    if ($cleaned -gt 0) {
        $leases.generated_at_utc = $nowUtc.ToString("o")
        Save-Leases -Data $leases
        Write-Output "NETTOYAGE: $cleaned bail(s) orphelin(s) marqué(s) comme expiré(s)."
    } else {
        Write-Output "NETTOYAGE: Aucun bail orphelin trouvé."
    }
}

# --- Garde-fou pré-écriture (T026) ---
function Test-BailDetenu {
    param([string]$Territory, [string]$ShardId)
    $lease = Get-ActiveLeaseForTerritory -Territory $Territory
    if (-not $lease) {
        return $false
    }
    if ($lease.holder_shard_id -ne $ShardId) {
        return $false
    }
    if (Is-LeaseExpired -Lease $lease) {
        return $false
    }
    return $true
}

# --- Rapport final ---
Write-Output "=============================================="
Write-Output "Action swarm : $Action"
Write-Output "Erreurs      : $($errors.Count)"
Write-Output "Avertissements: $($warnings.Count)"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  - $e" }
    exit 1
}

if ($warnings.Count -gt 0) {
    foreach ($w in $warnings) { Write-Output "  - $w" }
}

Write-Output "=============================================="
