#==============================================================================
# SKILL: pending-tab-sentinel
# Rôle: Détecter et éliminer les embryons de freeze UI.
# Surveille `tabOrder.local` dans agent-manager.json. Neutralise toute clé `pending:<uuid>`
# sans session validée.
# Couche CRUD — Nettoyage + Prévention.
#==============================================================================

[CmdletBinding()]
param(
    [string]$AgentManagerJsonPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\.kilo\agent-manager.json",  # obligatoire
    [switch]$ValidateSessions       # si true, vérifie que chaque pending:<uuid> correspond à une session active
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

if (-not (Test-Path -LiteralPath $AgentManagerJsonPath)) {
    Write-Output "[FAIL] agent-manager.json introuvable : $AgentManagerJsonPath"
    exit 2
}

# ── Lire le JSON ──
$jsonRaw = Get-Content -LiteralPath $AgentManagerJsonPath -Raw -ErrorAction SilentlyContinue
if (-not $jsonRaw) {
    Write-Output "[FAIL] Impossible de lire agent-manager.json"
    exit 2
}

try {
    $json = $jsonRaw | ConvertFrom-Json
} catch {
    Write-Output "[FAIL] Impossible de parser agent-manager.json : $($_.Exception.Message)"
    exit 2
}

# ── Collecter les IDs de session valides ──
$validSessionIds = @()
if ($json.sessions) {
    foreach ($sid in $json.sessions.PSObject.Properties.Name) {
        $validSessionIds += $sid
    }
}

# ── Analyser tabOrder.local ──
$tabOrderLocal = @()
if ($json.tabOrder -and $json.tabOrder.local) {
    $tabOrderLocal = @($json.tabOrder.local)
}

$pendingKeys = @()
$orphanSessions = @()
$neutralizedKeys = @()

foreach ($entry in $tabOrderLocal) {
    if ($entry -is [string] -and $entry -match "^pending:(.+)$") {
        $uuid = $matches[1]
        $pendingKeys += $entry

        $isValid = $false
        if ($ValidateSessions) {
            # Vérifier si l'UUID correspond à une session active
            foreach ($sid in $validSessionIds) {
                if ($sid -eq $uuid -or $sid -like "*$uuid*") {
                    $isValid = $true
                    break
                }
            }
        }

        if (-not $isValid) {
            $neutralizedKeys += $entry
            $orphanSessions += $uuid
            Write-Output "[NEUTRALISE] Clé pending supprimée : $entry (aucune session validée associée)"
        } else {
            Write-Output "[CONSERVE] Clé pending valide : $entry (session active : $uuid)"
        }
    }
}

# ── Nettoyer agent-manager.json ──
$cleaned = $false
if ($neutralizedKeys.Count -gt 0) {
    # Reconstruire tabOrder.local sans les clés neutralisées
    $newTabOrderLocal = @()
    foreach ($entry in $tabOrderLocal) {
        $isNeutralized = $false
        foreach ($nk in $neutralizedKeys) {
            if ($entry -eq $nk) {
                $isNeutralized = $true
                break
            }
        }
        if (-not $isNeutralized) {
            $newTabOrderLocal += $entry
        }
    }
    $json.tabOrder.local = $newTabOrderLocal
    $cleaned = $true

    # Écrire le JSON mis à jour
    $json | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $AgentManagerJsonPath -Encoding UTF8
    Write-Output "[INFO] agent-manager.json mis à jour : $($neutralizedKeys.Count) clé(s) pending neutralisée(s)"
}

# ── Rapport ──
$result = [PSCustomObject]@{
    Timestamp           = $timestamp
    AgentManagerJson    = $AgentManagerJsonPath
    PendingKeysFound    = $pendingKeys.Count
    PendingKeysNeutralized = $neutralizedKeys.Count
    OrphanSessions      = $orphanSessions
    Cleaned             = $cleaned
    Status              = if ($orphanSessions.Count -gt 0) { "CLEANED" } else { "OK" }
}

$jsonResult = $result | ConvertTo-Json -Depth 3
Write-Output $jsonResult

if ($orphanSessions.Count -gt 0) {
    Write-Output ""
    Write-Output "[OK] $($orphanSessions.Count) embryon(s) de freeze UI détecté(s) et neutralisé(s)."
    exit 0
} else {
    Write-Output ""
    Write-Output "[OK] Aucun embryon de freeze UI détecté. Interface saine."
    exit 0
}