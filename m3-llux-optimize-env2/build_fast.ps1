#!/usr/bin/env pwsh
# =============================================================================
# build-fast.ps1 — Build rapide de LLUX sur ENV2 (HP Z600)
#
# Optimisations appliquées :
#   - -Dcpu=westmere : cible le CPU E5620 (pas d'instructions AVX2 inexistantes)
#   - -Doptimize=ReleaseFast : optimisation standard pour le développement
#   - -j 16 : parallélisme sur tous les cœurs E5620 (16 threads)
#   - --cache-dir : cache Zig dans /tmp pour éviter les recompilations
# =============================================================================

$ErrorActionPreference = "Stop"

# Détecter le répertoire du script (doit être lancé depuis le dossier TALEX qui contient build.zig)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$zigExe = "zig"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BUILD RAPIDE LLUX - ENV2 (HP Z600)" -ForegroundColor Cyan
Write-Host "Répertoire : $scriptDir" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Vérifier que zig est disponible
if (-not (Get-Command zig -ErrorAction SilentlyContinue)) {
    Write-Error "zig n'est pas trouvé dans le PATH. Installez Zig ou ajoutez-le au PATH."
    exit 1
}

# Afficher la version de zig
zig version

# Lancer le build avec les flags optimisés ENV2
Write-Host "`n--- Lancement de zig build avec optimisations ENV2 ---" -ForegroundColor Yellow
$start = Get-Date

zig build `
    -Dcpu=westmere `
    -Doptimize=ReleaseFast `
    -j 16 `
    --cache-dir "$env:TEMP\zig-cache-llux"

$exitCode = $LASTEXITCODE
$end = Get-Date
$duration = ($end - $start).TotalSeconds

Write-Host "`n========================================" -ForegroundColor Cyan
if ($exitCode -eq 0) {
    Write-Host "BUILD RÉUSSI en $([math]::Round($duration, 2)) secondes" -ForegroundColor Green
} else {
    Write-Error "BUILD ÉCHOUÉ (code $exitCode) après $([math]::Round($duration, 2)) secondes"
    exit $exitCode
}
Write-Host "========================================" -ForegroundColor Cyan