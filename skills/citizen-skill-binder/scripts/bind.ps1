# scripts/bind.ps1
# citizen-skill-binder : lit CITIZENS.yaml et valide les competences d'un citizen
# Encodage CP1252 / ASCII

$ErrorActionPreference = "Stop"

param(
    [string]$CitizensPath = "D:\DO\WEB\TOOLS\L3-CITIZENS\LORX\citizens.yaml",
    [string]$CitizenId = "",
    [string]$SkillId = ""
)

function Write-Log {
    param([string]$Message)
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Write-Output "[$ts] $Message"
}

if (-not (Test-Path -LiteralPath $CitizensPath)) {
    Write-Log "ERREUR: CITIZENS.yaml introuvable : $CitizensPath"
    exit 1
}

Write-Log "Lecture CITIZENS.yaml : $CitizensPath"
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

Write-Log "Citoyens trouves : $($citizens.Count)"

$targets = $citizens
if ($CitizenId -ne "") {
    $targets = $citizens | Where-Object { $_.id -eq $CitizenId }
    if ($targets.Count -eq 0) {
        Write-Log "ERREUR: Citoyen introuvable : $CitizenId"
        exit 1
    }
}

$rbacMap = @{
    "versionnage" = @("citizen-skill-binder","citizen-credential-attestor");
    "combinaison" = @("citizen-skill-binder");
    "integration" = @("citizen-skill-binder","citizen-workload-dispatcher");
    "implementer" = @("citizen-skill-binder");
    "fournir" = @("citizen-workload-dispatcher");
}

foreach ($c in $targets) {
    Write-Log "=== Citoyen : $($c.id) ==="
    Write-Log "Role : $($c.role)"
    $authorized = @()
    foreach ($resp in $c.responsibilities) {
        $lower = $resp.ToLower()
        foreach ($key in $rbacMap.Keys) {
            if ($lower -like "*$key*") {
                foreach ($sk in $rbacMap[$key]) {
                    if (-not ($authorized -contains $sk)) { $authorized += $sk }
                }
            }
        }
    }
    Write-Log "Skills autorises : $($authorized -join ', ')"
    if ($SkillId -ne "") {
        if ($authorized -contains $SkillId) {
            Write-Log "RESULTAT: OK - $CitizenId est habilite pour $SkillId"
        } else {
            Write-Log "RESULTAT: REJETE - $CitizenId n'est pas habilite pour $SkillId"
        }
    }
}

Write-Log "Fin bind.ps1"
exit 0
