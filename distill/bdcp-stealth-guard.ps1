#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Garde-fou de furtivité BDCP (Phase 14, T131 à T134).

.DESCRIPTION
    Vérifie que le mode BDCP respecte les contraintes de furtivité :
    - Clapet BDCP V1 fermé par défaut (bdcp_clapet_default = "closed")
    - Aucune ouverture de nouvelle fenêtre Chromium
    - Lectures limitées aux périmètres de diagnostic autorisés (port 9222, 127.0.0.1)
    - Aucune requête réseau directe hors CDP

.PARAMETER ModeId
    Identifiant du mode actif (doit être "bdcp").

.PARAMETER TargetUrl
    URL cible de la requête CDP (doit être sur 127.0.0.1:9222).

.PARAMETER Operation
    Type d'opération (ex: new_tab, new_window, cdp_request, network_request).

.PARAMETER ClapetPath
    Chemin vers le fichier de configuration du clapet BDCP (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json).

.PARAMETER LogPath
    Chemin vers le journal des violations de furtivité (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\bdcp-stealth.log).

.EXAMPLE
    ./bdcp-stealth-guard.ps1 -ModeId bdcp -TargetUrl "http://127.0.0.1:9222/json" -Operation cdp_request

.EXAMPLE
    ./bdcp-stealth-guard.ps1 -ModeId bdcp -TargetUrl "https://example.com" -Operation network_request

.NOTES
    Phase 14, T131 à T134 — Garde-fou de furtivité BDCP
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModeId,

    [Parameter(Mandatory = $true)]
    [string]$TargetUrl,

    [Parameter(Mandatory = $true)]
    [string]$Operation,

    [string]$ClapetPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json",

    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\bdcp-stealth.log"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $ClapetPath)) {
    Write-Error "Fichier modes-matrix.json introuvable : $ClapetPath"
    exit 1
}

# --- Lecture de la matrice ---
$matrixContent = Get-Content -LiteralPath $ClapetPath -Raw -ErrorAction Stop
$matrix = $matrixContent | ConvertFrom-Json -ErrorAction Stop

# --- Trouver le mode bdcp ---
$bdcpMode = $matrix.modes | Where-Object { $_.mode_id -eq "bdcp" } | Select-Object -First 1
if (-not $bdcpMode) {
    Write-Error "Mode bdcp introuvable dans la matrice."
    exit 1
}

# --- T131 : Vérifier bdcp_clapet_default = "closed" ---
if ($bdcpMode.bdcp_clapet_default -ne "closed") {
    $errors += "T131_ECHEC : bdcp_clapet_default n'est pas 'closed' (valeur : $($bdcpMode.bdcp_clapet_default))"
}

# --- T132 : Vérifier qu'aucune nouvelle fenêtre n'est ouverte ---
if ($Operation -eq "new_window") {
    $errors += "T132_ECHEC : Ouverture de nouvelle fenêtre Chromium interdite en mode bdcp"
}

# --- T133 : Limiter les lectures aux périmètres de diagnostic autorisés ---
$allowedDiagnosticUrls = @(
    "http://127.0.0.1:9222/",
    "http://127.0.0.1:9222/json",
    "http://127.0.0.1:9222/json/version",
    "http://127.0.0.1:9222/json/new"
)
$isDiagnostic = $false
foreach ($allowedUrl in $allowedDiagnosticUrls) {
    if ($TargetUrl -eq $allowedUrl -or $TargetUrl -like "$allowedUrl*") {
        $isDiagnostic = $true
        break
    }
}
if (-not $isDiagnostic -and $Operation -in @("cdp_request", "network_request")) {
    $errors += "T133_ECHEC : URL cible $TargetUrl n'est pas dans les périmètres de diagnostic autorisés (port 9222, 127.0.0.1)"
}

# --- T134 : Tester la furtivité (aucune nouvelle fenêtre/navigation intrusive) ---
if ($Operation -in @("new_tab", "new_window")) {
    $errors += "T134_ECHEC : Création d'onglet/fenêtre interdite en mode bdcp (furtivité)"
}

# --- Journaliser la violation ---
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}
$logEntry = "[$nowUtc] Mode=$ModeId Operation=$Operation Target=$TargetUrl ClapetDefault=$($bdcpMode.bdcp_clapet_default) Decision=$([bool]::($errors.Count -eq 0)) Reason=$($errors -join '; ')"
Add-Content -LiteralPath $LogPath -Value $logEntry -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "BDCP STEALTH GUARD (T131 à T134)"
Write-Output "=============================================="
Write-Output "Mode        : $ModeId"
Write-Output "Opération   : $Operation"
Write-Output "Cible       : $TargetUrl"
Write-Output "Clapet BDCP : $($bdcpMode.bdcp_clapet_default)"
Write-Output "Décision    : $([bool]::($errors.Count -eq 0))"
Write-Output "Journal     : $LogPath"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    Write-Output "RESULTAT : FURTIVITÉ BDCP RESPECTÉE"
    exit 0
}
