# scripts/dispatch.ps1
# citizen-workload-dispatcher : routage d'intention vers un citizen L3
# Encodage CP1252 / ASCII

$ErrorActionPreference = "Stop"

param(
    [string]$Intent = "",
    [string]$CitizensPath = "D:\DO\WEB\TOOLS\L3-CITIZENS\LORX\citizens.yaml",
    [double]$Threshold = 0.5
)

function Write-Log {
    param([string]$Message)
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Write-Output "[$ts] $Message"
}

if ([string]::IsNullOrWhiteSpace($Intent)) {
    Write-Log "ERREUR: intention vide"
    exit 1
}

if (-not (Test-Path -LiteralPath $CitizensPath)) {
    Write-Log "ERREUR: CITIZENS.yaml introuvable : $CitizensPath"
    exit 1
}

Write-Log "Intention : $Intent"
$raw = Get-Content -LiteralPath $CitizensPath -Raw -Encoding Default

$citizens = @()
$current = $null
$inCitizen = $false
foreach ($line in $raw -split "`n") {
    $trim = $line.Trim()
    if ($trim -match '^-\s+id:\s*"?(?<id>[^"]+)"?') {
        if ($current) { $citizens += $current }
        $current = @{ id = $matches['id']; role = ""; responsibilities = @() }
        $inCitizen = $true
        continue
    }
    if ($inCitizen -and $trim -match '^role:\s*"?(?<val>[^"]+)"?') {
        $current.role = $matches['val']
        continue
    }
    if ($inCitizen -and $trim -match '^\s+-\s+"?(?<val>[^"]+)"?') {
        $current.responsibilities += $matches['val']
        continue
    }
}
if ($current) { $citizens += $current }

$intentLower = $Intent.ToLower()
$scores = @()
foreach ($c in $citizens) {
    $score = 0.0
    $blob = (($c.role + " " + ($c.responsibilities -join " ")).ToLower())
    foreach ($w in $intentLower -split '\s+') {
        if ($w.Length -gt 2 -and $blob -like "*$w*") { $score += 0.2 }
    }
    $scores += @{ id = $c.id; score = [math]::Round($score,2) }
}

$scores = $scores | Sort-Object score -Descending
$best = $scores[0]
Write-Log "Citoyens classes :"
foreach ($s in $scores) { Write-Log "  $($s.id) : score=$($s.score)" }

if ($best.score -ge $Threshold) {
    Write-Log "RESULTAT: ROUTE vers $($best.id) (score=$($best.score))"
    exit 0
} else {
    Write-Log "RESULTAT: NO_MATCH (meilleur score=$($best.score) < seuil=$Threshold)"
    exit 2
}
