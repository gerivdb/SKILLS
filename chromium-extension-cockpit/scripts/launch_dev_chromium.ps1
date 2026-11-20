#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
# launch_dev_chromium.ps1 — Lancement d'une instance Chromium isolée pour le développement d'extensions.
#
# Démarre Chromium avec :
#   --user-data-dir=D:\DO\WEB\TOOLS\DEV_CHROMIUM_PROFILE  (profil isolé, préserve les profils utilisateurs)
#   --remote-debugging-port=9222                          (port CDP pour le cockpit et les scripts)
#
# Usage : .\launch_dev_chromium.ps1
#         .\launch_dev_chromium.ps1 -Port 9222 -Profile "D:\DO\WEB\TOOLS\DEV_CHROMIUM_PROFILE"

param(
    [string]$Port = 9222,
    [string]$Profile = "D:\DO\WEB\TOOLS\DEV_CHROMIUM_PROFILE",
    [switch]$NoFirstRun
)

# Détecter le binaire Chrome/Chromium
$chromeCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "C:\Program Files\Chromium\Application\chrome.exe",
    "C:\Program Files (x86)\Chromium\Application\chrome.exe",
    "C:\Users\${env:USERNAME}\AppData\Local\Google\Chrome\Application\chrome.exe"
)

$chromeExe = $null
foreach ($c in $chromeCandidates) {
    if (Test-Path -LiteralPath $c) {
        $chromeExe = $c
        break
    }
}

if (-not $chromeExe) {
    Write-Error "Aucun binaire Chrome/Chromium trouvé. Installez Chrome ou Chromium."
    exit 1
}

# Créer le dossier de profil s'il n'existe pas
if (-not (Test-Path -LiteralPath $Profile)) {
    New-Item -ItemType Directory -Force -Path $Profile | Out-Null
    Write-Host "[INFO] Profil de développement créé : $Profile"
}

# Construire les arguments
$args = @(
    "--remote-debugging-port=$Port",
    "--user-data-dir=$Profile",
    "--no-first-run",
    "--no-default-browser-check"
)

if ($NoFirstRun) {
    $args += "--no-first-run"
}

Write-Host "[INFO] Lancement de Chromium de développement..."
Write-Host "[INFO] Binaire : $chromeExe"
Write-Host "[INFO] Profil  : $Profile"
Write-Host "[INFO] Port CDP: $Port"
Write-Host "[INFO] Attendez que la fenêtre s'affiche, puis ouvrez chrome://extensions"

# Lancer Chromium (processus détaché, ne pas attendre)
Start-Process -FilePath $chromeExe -ArgumentList $args

Write-Host "[SUCCÈS] Chromium lancé. Port CDP $Port disponible pour le cockpit."
