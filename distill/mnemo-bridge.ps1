#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Pont épisodique Mnemo — écrit une trace d'exécution de skill dans Mnemo (Phase 7, T061-T065).

.DESCRIPTION
    Enregistre dans Mnemo (mémoire épisodique persistante, worker HTTP 37777,
    SQLite + Chroma) une trace structurée de l'exécution d'un skill, pour
    permettre la réactivation inter-shards depuis la mémoire épisodique.

.PARAMETER SkillName
    Nom du skill exécuté.

.PARAMETER Result
    Résultat : succes | echec | contourne.

.PARAMETER ShardId
    Identifiant du shard (défaut: ENV2).

.PARAMETER MnemoWorkerUrl
    URL du worker HTTP Mnemo (défaut: http://127.0.0.1:37777).

.PARAMETER EvidencePath
    Chemin vers le fichier EVIDENCE.md du skill.

.EXAMPLE
    ./mnemo-bridge.ps1 -SkillName chromium-profile-2 -Result succes -ShardId ENV2

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md, SPEC-SKILL-FORMAT.md
    Mnemo: D:\DO\WEB\TOOLS\L4-TOOLS\Mnemo (fork de Claude-Mem)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillName,

    [Parameter(Mandatory = $true)]
    [ValidateSet("succes", "echec", "contourne")]
    [string]$Result,

    [string]$ShardId = "ENV2",

    [string]$MnemoWorkerUrl = "http://127.0.0.1:37777",

    [string]$EvidencePath
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if ($EvidencePath -and -not (Test-Path -LiteralPath $EvidencePath)) {
    Write-Warning "Fichier EVIDENCE introuvable : $EvidencePath"
}

# --- Construction de la trace épisodique ---
$trace = [PSCustomObject]@{
    timestamp_utc = $nowUtc
    skill_name = $SkillName
    result = $Result
    shard_id = $ShardId
    source = "kilo_skill_execution"
    evidence_path = $EvidencePath
    intent_hash = $null
}

# Tenter de lire l'intent_hash depuis le SKILL.md
$skillFolder = Join-Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills" $SkillName
$skillFile = Join-Path $skillFolder "SKILL.md"
if (Test-Path -LiteralPath $skillFile) {
    $skillContent = Get-Content -LiteralPath $skillFile -Raw -ErrorAction SilentlyContinue
    if ($skillContent) {
        $match = [regex]::Match($skillContent, '(?m)^intent_hash:\s*(.+)$')
        if ($match.Success) {
            $trace.intent_hash = $match.Groups[1].Value.Trim().Trim('"')
        }
    }
}

# --- Envoi au worker HTTP Mnemo ---
try {
    $jsonBody = $trace | ConvertTo-Json -Depth 3
    $response = Invoke-RestMethod -Uri "$MnemoWorkerUrl/api/episode" -Method POST -ContentType "application/json" -Body $jsonBody -TimeoutSec 10 -ErrorAction Stop
    Write-Output "MNEMO : Trace épisodique écrite (réponse: $($response.status))"
}
catch {
    $warnings += "MNEMO_ECHEC: Impossible d'écrire dans le worker Mnemo ($MnemoWorkerUrl). Erreur: $($_.Exception.Message)"
    Write-Warning "MNEMO : Worker non joignable. La trace sera enregistrée localement uniquement."
    # Sauvegarde locale de la trace en attendant
    $localTracePath = Join-Path (Split-Path -Parent $skillFolder) "logs" "mnemo-pending-$SkillName-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ')).json"
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $localTracePath))) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $localTracePath) | Out-Null
    }
    $jsonBody | Set-Content -LiteralPath $localTracePath -Encoding UTF8
    Write-Output "MNEMO : Trace sauvegardée localement : $localTracePath"
}

# --- Rapport ---
Write-Output "=============================================="
Write-output "PONT ÉPISODIQUE MNEMO"
Write-Output "=============================================="
Write-Output "Skill   : $SkillName"
Write-Output "Résultat: $Result"
Write-Output "Shard   : $ShardId"
Write-Output "Intent  : $($trace.intent_hash)"
Write-Output "=============================================="

if ($warnings.Count -gt 0) {
    foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
}

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
}
