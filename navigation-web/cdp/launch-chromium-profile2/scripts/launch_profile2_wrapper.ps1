#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
# launch_profile2_wrapper.ps1 — Wrapper du skill launch-chromium-profile2
# Appelle le script canonique launch_profile2.ps1 du cockpit CDP.

$ErrorActionPreference = "Stop"

$scriptPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\navigation-web\cdp\chromium-extension-cockpit\scripts\launch_profile2.ps1"

if (-not (Test-Path -LiteralPath $scriptPath)) {
    Write-Error "[ERREUR] Script canonique introuvable : $scriptPath"
    exit 1
}

Write-Host "[INFO] Invocation du script canonique launch_profile2.ps1..."
& pwsh -File $scriptPath
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "[SUCCÈS] Chromium Profil 2 opérationnel (port 9222)."
} else {
    Write-Error "[ERREUR] Échec du lancement Chromium (code $exitCode)."
}

exit $exitCode
