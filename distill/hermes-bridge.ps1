#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Pont HERMES — écrit des faits clés dans le graphe de connaissances fédéré (Phase 7, T066-T070).

.DESCRIPTION
    Enregistre dans HERMES (API REST port 8788, facts.db + vector_store) les
    faits clés issus de l'exécution d'un skill, pour les rendre accessibles
    depuis tous les shards de l'écosystème gerivdb.

.PARAMETER FactKey
    Clé du fait (ex: "skill:chromium-profile-2:status").

.PARAMETER FactValue
    Valeur du fait (ex: "active", "echec", "score_utilite: -3").

.PARAMETER FactType
    Type de fait (ex: "skill_status", "skill_score", "skill_usage").

.PARAMETER ShardId
    Identifiant du shard (défaut: ENV2).

.PARAMETER HermesUrl
    URL de l'API REST HERMES (défaut: http://127.0.0.1:8788).

.EXAMPLE
    ./hermes-bridge.ps1 -FactKey "skill:chromium-profile-2:status" -FactValue "active" -FactType "skill_status"

.EXAMPLE
    ./hermes-bridge.ps1 -FactKey "skill:distill-skill:score" -FactValue "-3" -FactType "skill_score"

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md, SPEC-SKILL-FORMAT.md
    HERMES: D:\DO\WEB\TOOLS\L0-CANON\HERMES (API REST 8788, facts.db, vector_store)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$FactKey,

    [Parameter(Mandatory = $true)]
    [string]$FactValue,

    [Parameter(Mandatory = $true)]
    [string]$FactType,

    [string]$ShardId = "ENV2",

    [string]$HermesUrl = "http://127.0.0.1:8788"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Construction du fait ---
$fact = [PSCustomObject]@{
    timestamp_utc = $nowUtc
    fact_key = $FactKey
    fact_value = $FactValue
    fact_type = $FactType
    shard_id = $ShardId
    source = "kilo_skill_execution"
}

# --- Envoi à l'API REST HERMES ---
try {
    $jsonBody = $fact | ConvertTo-Json -Depth 3
    $response = Invoke-RestMethod -Uri "$HermesUrl/api/facts" -Method POST -ContentType "application/json" -Body $jsonBody -TimeoutSec 10 -ErrorAction Stop
    Write-Output "HERMES : Fact écrit (réponse: $($response.status))"
}
catch {
    $warnings += "HERMES_ECHEC: Impossible d'écrire dans l'API HERMES ($HermesUrl). Erreur: $($_.Exception.Message)"
    Write-Warning "HERMES : API non joignable. Le fait sera enregistré localement uniquement."
    # Sauvegarde locale de la trace en attendant
    $localFactPath = Join-Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" "hermes-pending-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ')).json"
    if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
        New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
    }
    $jsonBody | Set-Content -LiteralPath $localFactPath -Encoding UTF8
    Write-Output "HERMES : Fact sauvegardé localement : $localFactPath"
}

# --- Rapport ---
Write-Output "=============================================="
Write-output "PONT HERMES — GRAPHE DE CONNAISSANCES"
Write-Output "=============================================="
Write-Output "Clé      : $FactKey"
Write-Output "Valeur   : $FactValue"
Write-Output "Type     : $FactType"
Write-Output "Shard    : $ShardId"
Write-Output "=============================================="

if ($warnings.Count -gt 0) {
    foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
}

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
}
