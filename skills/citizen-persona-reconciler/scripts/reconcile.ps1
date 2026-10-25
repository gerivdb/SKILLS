# scripts/reconcile.ps1
# citizen-persona-reconciler : aligne persona agent (kilo.json) avec citizen L3
# Encodage CP1252 / ASCII

$ErrorActionPreference = "Stop"

param(
    [string]$KiloJson = "C:\Users\GG\.kilo\kilo.json",
    [string]$CitizensPath = "D:\DO\WEB\TOOLS\L3-CITIZENS\LORX\citizens.yaml",
    [string]$CitizenId = ""
)

function Write-Log {
    param([string]$Message)
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Write-Output "[$ts] $Message"
}

if (-not (Test-Path -LiteralPath $KiloJson)) {
    Write-Log "ERREUR: kilo.json introuvable : $KiloJson"
    exit 1
}
if (-not (Test-Path -LiteralPath $CitizensPath)) {
    Write-Log "ERREUR: CITIZENS.yaml introuvable : $CitizensPath"
    exit 1
}

Write-Log "Reconciliation persona agent <=> citizen L3"
$kilo = Get-Content -LiteralPath $KiloJson -Raw -Encoding Default
$raw = Get-Content -LiteralPath $CitizensPath -Raw -Encoding Default

$citizen = $null
$current = $null
$inCitizen = $false
foreach ($line in $raw -split "`n") {
    $trim = $line.Trim()
    if ($trim -match '^-\s+id:\s*"?(?<id>[^"]+)"?') {
        if ($current -and $current.id -eq $CitizenId) { $citizen = $current }
        $current = @{ id = $matches['id']; role = ""; style = ""; forbidden = @() }
        $inCitizen = $true
        continue
    }
    if ($inCitizen -and $trim -match '^role:\s*"?(?<val>[^"]+)"?') { $current.role = $matches['val']; continue }
    if ($inCitizen -and $trim -match '^communication_style:\s*"?(?<val>[^"]+)"?') { $current.style = $matches['val']; continue }
    if ($inCitizen -and $trim -match '^\s+-\s+"?(?<val>[^"]+)"?') { $current.forbidden += $matches['val']; continue }
}
if ($current -and $current.id -eq $CitizenId) { $citizen = $current }

if (-not $citizen) {
    Write-Log "ERREUR: citizen introuvable : $CitizenId"
    exit 1
}

Write-Log "Citizen : $($citizen.id) | role=$($citizen.role) | style=$($citizen.style)"
$gaps = @()
$score = 1.0
$kiloLower = $kilo.ToLower()
if ($citizen.role -and $kiloLower -notlike "*$($citizen.role.ToLower())*") { $gaps += "role non reflechi dans kilo.json"; $score -= 0.3 }
if ($citizen.style -and $kiloLower -notlike "*$($citizen.style.ToLower())*") { $gaps += "communication_style non reflechi dans kilo.json"; $score -= 0.3 }
foreach ($f in $citizen.forbidden) {
    if ($kiloLower -notlike "*$($f.ToLower())*") { $gaps += "interdit '$f' absent de kilo.json"; $score -= 0.1 }
}
if ($score -lt 0) { $score = 0 }
$score = [math]::Round($score,2)

if ($gaps.Count -eq 0) {
    Write-Log "RESULTAT: ALIGNE - score=$score"
    exit 0
} else {
    Write-Log "RESULTAT: ECARTE - score=$score"
    foreach ($g in $gaps) { Write-Log "  ecart: $g" }
    exit 1
}
