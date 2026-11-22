#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
# launch_profile2.ps1 — Lanceur persistant du Profil 2 Chromium (Vrais cookies + Port CDP 9222).
#
# Utilise WMI (Win32_Process) pour détacher le processus du Job Object de Windows
# afin d'éviter que la fin de la tâche VS Code ne tue le navigateur.

$port = 9222
$cdpUrl = "http://127.0.0.1:$port"

# 1. Vérifier si le port est déjà actif
try {
    $v = Invoke-RestMethod -Uri "$cdpUrl/json/version" -TimeoutSec 1 -ErrorAction Stop
    Write-Host "[OK] Chromium Profil 2 est déjà actif sur le port $port ($($v.Browser))."
    exit 0
} catch {}

Write-Host "[INFO] Port $port fermé. Préparation du lancement de Profil 2..."

$chromeExe = "C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe"
$userData = "C:\Users\GG\AppData\Local\Chromium\User Data"
$profileDir = "Profile 2"
$profilePath = Join-Path $userData $profileDir

if (-not (Test-Path $profilePath)) {
    Write-Error "[ERREUR] Le dossier Profil 2 n'existe pas : $profilePath"
    exit 1
}

# 2. Purge des verrous LOCK orphelins (taille 0)
$orphanLocks = Get-ChildItem -Path $profilePath -Recurse -Filter "LOCK" -ErrorAction SilentlyContinue | Where-Object { $_.Length -eq 0 }
if ($orphanLocks) {
    Write-Host "[INFO] Purge de $($orphanLocks.Count) verrous LOCK orphelins..."
    foreach ($l in $orphanLocks) {
        Remove-Item -LiteralPath $l.FullName -Force -ErrorAction SilentlyContinue
    }
}

# 3. Réparation de exit_type dans Preferences
$prefsFile = Join-Path $profilePath "Preferences"
if (Test-Path $prefsFile) {
    try {
        $json = Get-Content -LiteralPath $prefsFile -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($json.profile.exit_type -eq "Crashed") {
            $json.profile.exit_type = "Normal"
            $json | ConvertTo-Json -Depth 100 -Compress | Set-Content -LiteralPath $prefsFile -Encoding UTF8
            Write-Host "[INFO] Preferences réparé : exit_type = Normal."
        }
    } catch {}
}

# 4. Lancement détaché via WMI (échappe au Job Object Windows)
$cmdLine = "`"$chromeExe`" --profile-directory=`"$profileDir`" --remote-debugging-port=$port --remote-allow-origins=*"
$wmi = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmdLine }

if ($wmi.ReturnValue -ne 0) {
    Write-Error "[ERREUR] Échec du lancement WMI (code $($wmi.ReturnValue))."
    exit 1
}

Write-Host "[INFO] Processus Chromium démarré (PID $($wmi.ProcessId)). Attente du socket CDP..."

# 5. Attente active de la disponibilité du port
$ready = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Milliseconds 400
    try {
        $v = Invoke-RestMethod -Uri "$cdpUrl/json/version" -TimeoutSec 1 -ErrorAction Stop
        if ($v.Browser) {
            $ready = $true
            Write-Host "[SUCCÈS] Chromium Profil 2 opérationnel sur le port $port ($($v.Browser))."
            break
        }
    } catch {}
}

if (-not $ready) {
    Write-Error "[ERREUR] Le port $port n'a pas répondu dans les 6 secondes."
    exit 1
}
