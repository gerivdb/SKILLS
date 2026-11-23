#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Garde-fou de budget et sobriété du profil FREE (Phase 14, T135 à T139).

.DESCRIPTION
    Vérifie que le mode FREE respecte les contraintes de budget et de furtivité :
    - Plafond strict de contexte/sortie
    - Exclusion absolue des endpoints payants ou lourds
    - Sobriété du nombre de requêtes et de la taille de contexte

.PARAMETER ModeId
    Identifiant du mode actif (doit être "free").

.PARAMETER TargetUrl
    URL cible de la requête.

.PARAMETER Operation
    Type d'opération (ex: http_request, cdp_request, file_read).

.PARAMETER ContextSize
    Taille du contexte en octets (pour vérifier le plafond).

.PARAMETER BudgetPath
    Chemin vers le fichier de configuration du budget FREE (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\free-budget.json).

.PARAMETER LogPath
    Chemin vers le journal des violations de budget (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\free-budget.log).

.EXAMPLE
    ./free-budget-guard.ps1 -ModeId free -TargetUrl "https://api.example.com" -Operation http_request -ContextSize 5000

.EXAMPLE
    ./free-budget-guard.ps1 -ModeId free -TargetUrl "http://127.0.0.1:9222/json" -Operation cdp_request -ContextSize 1000

.NOTES
    Phase 14, T135 à T139 — Garde-fou de budget FREE
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModeId,

    [Parameter(Mandatory = $true)]
    [string]$TargetUrl,

    [Parameter(Mandatory = $true)]
    [string]$Operation,

    [Parameter(Mandatory = $true)]
    [int]$ContextSize,

    [string]$BudgetPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\free-budget.json",

    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\free-budget.log"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $BudgetPath)) {
    Write-Error "Fichier free-budget.json introuvable : $BudgetPath"
    exit 1
}

# --- Lecture du budget FREE ---
$budgetContent = Get-Content -LiteralPath $BudgetPath -Raw -ErrorAction Stop
$budget = $budgetContent | ConvertFrom-Json -ErrorAction Stop

# --- T135 : Vérifier le plafond de contexte/sortie ---
$maxContextSize = $budget.maxContextSizeBytes
if ($ContextSize -gt $maxContextSize) {
    $errors += "T135_ECHEC : Taille de contexte $ContextSize octets dépasse le plafond $maxContextSize octets du mode FREE"
}

# --- T136 : Exclure absolument les endpoints payants ou lourds ---
$blockedEndpoints = $budget.blockedEndpoints
$isBlocked = $false
foreach ($blocked in $blockedEndpoints) {
    if ($TargetUrl -like "*$blocked*") {
        $isBlocked = $true
        break
    }
}
if ($isBlocked) {
    $errors += "T136_ECHEC : Endpoint $TargetUrl est bloqué en mode FREE (endpoint payant ou lourd)"
}

# --- T137 : Tester le budget FREE (nombre de requêtes, taille de contexte) ---
$maxRequests = $budget.maxRequestsPerSession
$currentRequests = $budget.currentRequestsCount
if (($currentRequests + 1) -gt $maxRequests) {
    $errors += "T137_ECHEC : Nombre de requêtes $($currentRequests + 1) dépasse le maximum $maxRequests par session en mode FREE"
}

# --- T138 : Corriger l'écart de chemin canonique ---
$canonicalPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
$wrongPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS"
if ($TargetUrl -like "*$wrongPath*") {
    $errors += "T138_ECHEC : Chemin non canonique détecté ($TargetUrl). Utiliser $canonicalPath à la place de $wrongPath"
}

# --- T139 : Tester la sobriété du profil FREE ---
if ($ContextSize -gt ($maxContextSize * 0.8)) {
    $warnings += "T139_WARN : Taille de contexte $ContextSize octets approche le plafond $maxContextSize octets (80% dépassé)"
}

# --- Journaliser la violation ---
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}
$logEntry = "[$nowUtc] Mode=$ModeId Operation=$Operation Target=$TargetUrl ContextSize=$ContextSize Decision=$([bool]::($errors.Count -eq 0)) Reason=$($errors -join '; ')"
Add-Content -LiteralPath $LogPath -Value $logEntry -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "FREE BUDGET GUARD (T135 à T139)"
Write-Output "=============================================="
Write-Output "Mode        : $ModeId"
Write-Output "Opération   : $Operation"
Write-Output "Cible       : $TargetUrl"
Write-Output "Contexte    : $ContextSize octets (plafond : $maxContextSize octets)"
Write-Output "Décision    : $([bool]::($errors.Count -eq 0))"
Write-Output "Journal     : $LogPath"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
    exit 1
} else {
    if ($warnings.Count -gt 0) {
        foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
    }
    Write-Output "RESULTAT : BUDGET FREE RESPECTÉ"
    exit 0
}
