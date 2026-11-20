#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
# launch_micro_sandbox.ps1 — Lanceur de micro-sandbox éphémère pour tests d'extension Chromium.
#
# Démarre une instance Chromium/Ungoogled-Chromium isolée avec :
#   --user-data-dir=C:\Temp\ugc_sandbox_<ext_name>   (profil jetable)
#   --load-extension=<ExtensionPath>                 (extension montée en dev)
#   --remote-debugging-port=<Port>                   (port CDP pour le cockpit)
#   --no-first-run --no-default-browser-check
#
# Usage : .\launch_micro_sandbox.ps1 -ExtensionPath "D:\...\sidekeep-x" -Port 9223
#         .\launch_micro_sandbox.ps1 -ExtensionPath "D:\...\sidekeep-x" -Port 9223 -Clean

param(
    [Parameter(Mandatory=$true)]
    [string]$ExtensionPath,

    [Parameter(Mandatory=$true)]
    [int]$Port,

    [switch]$Clean
)

# Détecter l'exécutable Chromium/Ungoogled-Chromium
$chromiumCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "C:\Program Files\Chromium\Application\chrome.exe",
    "C:\Program Files (x86)\Chromium\Application\chrome.exe",
    "C:\Users\${env:USERNAME}\AppData\Local\Google\Chrome\Application\chrome.exe",
    "C:\Program Files\Ungoogled-Chromium\Application\chrome.exe",
    "C:\Program Files (x86)\Ungoogled-Chromium\Application\chrome.exe"
)

$chromiumExe = $null
foreach ($c in $chromiumCandidates) {
    if (Test-Path -LiteralPath $c) {
        $chromiumExe = $c
        break
    }
}

if (-not $chromiumExe) {
    Write-Error "Aucun binaire Chromium/Chrome trouvé. Installez Chromium, Chrome ou Ungoogled-Chromium."
    exit 1
}

# Valider le chemin de l'extension
if (-not (Test-Path -LiteralPath $ExtensionPath)) {
    Write-Error "Le dossier de l'extension est introuvable : $ExtensionPath"
    exit 1
}

# Construire le nom du dossier sandbox depuis le nom de l'extension
$extName = Split-Path -Leaf $ExtensionPath
$sandboxDir = Join-Path "C:\Temp" "ugc_sandbox_${extName}"

# Option --Clean : supprimer le profil sandbox existant
if ($Clean -and (Test-Path -LiteralPath $sandboxDir)) {
    Remove-Item -Recurse -Force -LiteralPath $sandboxDir
    Write-Host "[INFO] Profil sandbox supprimé : $sandboxDir"
}

# Créer le dossier sandbox s'il n'existe pas
if (-not (Test-Path -LiteralPath $sandboxDir)) {
    New-Item -ItemType Directory -Force -Path $sandboxDir | Out-Null
    Write-Host "[INFO] Profil sandbox créé : $sandboxDir"
}

# Construire les arguments de lancement
$args = @(
    "--user-data-dir=$sandboxDir",
    "--load-extension=$ExtensionPath",
    "--remote-debugging-port=$Port",
    "--no-first-run",
    "--no-default-browser-check"
)

Write-Host "[INFO] Lancement de la micro-sandbox Chromium..."
Write-Host "[INFO] Binaire   : $chromiumExe"
Write-Host "[INFO] Extension : $ExtensionPath"
Write-Host "[INFO] Profil    : $sandboxDir"
Write-Host "[INFO] Port CDP  : $Port"

# Lancer Chromium (processus détaché)
Start-Process -FilePath $chromiumExe -ArgumentList $args

Write-Host "[SUCCÈS] Micro-sandbox lancée. Port CDP $Port disponible pour le cockpit."
Write-Host "[INFO] Attendez que la fenêtre s'affiche, puis vérifiez chrome://extensions"
