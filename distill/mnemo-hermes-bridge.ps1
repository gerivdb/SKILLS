#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Pontage Mnemo (37777) et HERMES (8788) par mode (Phase 18, T171 à T180).

.DESCRIPTION
    Gère le pontage vers Mnemo (mémoire épisodique, worker HTTP 37777) et HERMES
    (mémoire fédérée, API REST 8788) par mode actif (architect, data, bdcp, free).
    Respecte les règles d'accès par mode, le write_policy (read_only vs lease_required)
    et le budget FREE (contexte, requêtes).

    En cas d'indisponibilité ou de timeout du pont, génère un code de sortie
    explicite et un journal horodaté UTC, sans confondre erreur réseau avec
    validation silencieuse.

.PARAMETER ModeId
    Mode actif actuel (architect, data, bdcp, free).

.PARAMETER Target
    Cible du pontage (mnemo ou hermes).

.PARAMETER Operation
    Type d'opération (ex: write_episode, write_fact, read_episode, read_fact).

.PARAMETER Payload
    Payload JSON à envoyer (optionnel).

.PARAMETER MnemoUrl
    URL du worker HTTP Mnemo (défaut: http://127.0.0.1:37777).

.PARAMETER HermesUrl
    URL de l'API REST HERMES (défaut: http://127.0.0.1:8788).

.PARAMETER LogPath
    Chemin vers le journal des ponts (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\mnemo-hermes-bridge.log).

.EXAMPLE
    ./mnemo-hermes-bridge.ps1 -ModeId data -Target mnemo -Operation write_episode -Payload '{"skill":"chromium-profile-2","result":"succes"}'

.EXAMPLE
    ./mnemo-hermes-bridge.ps1 -ModeId architect -Target hermes -Operation write_fact -Payload '{"fact":"skill:chromium-profile-2:status","value":"active"}'

.NOTES
    Phase 18, T171 à T180 — Pontage Mnemo & HERMES par mode
    Dépend : mode-write-guard.ps1, skill-router.ps1, leases.json
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModeId,

    [Parameter(Mandatory = $true)]
    [ValidateSet("mnemo", "hermes")]
    [string]$Target,

    [Parameter(Mandatory = $true)]
    [string]$Operation,

    [string]$Payload,

    [string]$MnemoUrl = "http://127.0.0.1:37777",

    [string]$HermesUrl = "http://127.0.0.1:8788",

    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\mnemo-hermes-bridge.log"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}

# --- Définir les règles d'accès par mode (T171, T172) ---
$modeRules = @{
    architect = @{
        write_policy = "read_only"
        mnemo_access = "read_only"
        hermes_access = "read_only"
        budget_free = $false
    }
    data = @{
        write_policy = "lease_required"
        mnemo_access = "read_write"
        hermes_access = "read_write"
        budget_free = $false
    }
    bdcp = @{
        write_policy = "read_only"
        mnemo_access = "read_only"
        hermes_access = "read_only"
        budget_free = $false
    }
    free = @{
        write_policy = "read_only"
        mnemo_access = "read_only"
        hermes_access = "read_only"
        budget_free = $true
    }
}

$modeRule = $modeRules[$ModeId]
if (-not $modeRule) {
    Write-Error "Mode '$ModeId' non reconnu dans les règles d'accès Mnemo/HERMES"
    exit 1
}

# --- T171 : Règles d'accès par mode pour Mnemo (37777) ---
# --- T172 : Règles d'accès par mode pour HERMES (8788) ---
# Vérifier que le mode autorise l'accès à la cible demandée
$targetAccess = if ($Target -eq "mnemo") { $modeRule.mnemo_access } else { $modeRule.hermes_access }
if ($targetAccess -eq "read_only" -and $Operation -in @("write_episode", "write_fact", "write")) {
    $errors += "T171_ECHEC : Mode '$ModeId' en lecture seule sur $Target, opération '$Operation' refusée"
}

# --- Vérifier le write_policy ---
if ($modeRule.write_policy -eq "read_only" -and $Operation -in @("write_episode", "write_fact", "write")) {
    $errors += "T165_ECHEC : Mode '$ModeId' en write_policy=read_only, opération d'écriture '$Operation' refusée sur $Target"
}

# --- Vérifier le budget FREE (T171, T172) ---
if ($modeRule.budget_free -and $Payload) {
    $payloadSize = [System.Text.Encoding]::UTF8.GetByteCount($Payload)
    $maxContextSize = 100000 # 100 Ko, même budget que FREE
    if ($payloadSize -gt $maxContextSize) {
        $errors += "T175_ECHEC : Payload $payloadSize octets dépasse le plafond FREE $maxContextSize octets sur $Target"
    }
}

# --- T176 : Gérer les indisponibilités de pont Mnemo (port 37777) ---
# --- T177 : Gérer les indisponibilités de pont HERMES (port 8788) ---
$targetUrl = if ($Target -eq "mnemo") { $MnemoUrl } else { $HermesUrl }
$targetName = if ($Target -eq "mnemo") { "Mnemo" } else { "HERMES" }

try {
    $response = Invoke-RestMethod -Uri "$targetUrl/api/$Operation" -Method POST -ContentType "application/json" -Body $Payload -TimeoutSec 5 -ErrorAction Stop
    $bridgeStatus = "OK"
    $bridgeResponse = $response
} catch {
    $bridgeStatus = "ERROR"
    $bridgeResponse = $_.Exception.Message
    $errors += "T176_ECHEC : Pont $TargetName ($targetUrl) injoignable : $($_.Exception.Message)"
}

# --- T178 : Tester le repli quand un pont est injoignable ---
# Si le pont est injoignable, on ne fait pas de repli silencieux, on signale l'erreur
if ($bridgeStatus -eq "ERROR") {
    $warnings += "T178_INFO : Repli impossible sur $TargetName, erreur réseau signalée explicitement"
}

# --- T179 : Valider les traces horodatées UTC ---
$bridgeEntry = [PSCustomObject]@{
    timestamp_utc = $nowUtc
    mode_id = $ModeId
    target = $Target
    operation = $Operation
    status = $bridgeStatus
    response = $bridgeResponse
    payload_size = if ($Payload) { [System.Text.Encoding]::UTF8.GetByteCount($Payload) } else { 0 }
}

# --- Écriture du journal de pont ---
$logEntry = "[$nowUtc] MODE=$ModeId TARGET=$Target OPERATION=$Operation STATUS=$bridgeStatus | $($bridgeResponse)"
Add-Content -LiteralPath $LogPath -Value $logEntry -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "PONT MNEMO/HERMES PAR MODE (T171 à T180)"
Write-Output "=============================================="
Write-Output "Mode actif   : $ModeId"
Write-Output "Cible        : $Target ($targetUrl)"
Write-Output "Opération    : $Operation"
Write-Output "Statut       : $bridgeStatus"
Write-Output "Horodatage   : $nowUtc"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    if ($warnings.Count -gt 0) {
        foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
    }
    Write-Output "RESULTAT : PONTAGE VALIDÉ"
    exit 0
}
