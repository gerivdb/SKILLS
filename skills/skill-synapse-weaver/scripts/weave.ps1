#==============================================================================
# SKILL: skill-synapse-weaver
# Rôle: Tisseur topologique — déduit les Combos et détecte les impasses.
# Couche: Méta-Skills & Cycle de Vie
#==============================================================================

[CmdletBinding()]
param(
    [string]$SkillsRepo = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS",
    [string]$OutputPath = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\weave-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# Découvrir tous les skills
$skillDirs = Get-ChildItem -LiteralPath (Join-Path $SkillsRepo "skills") -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

$skills = @()
foreach ($d in $skillDirs) {
    $content = Get-Content -LiteralPath (Join-Path $d.FullName "SKILL.md") -Raw -ErrorAction SilentlyContinue
    $inputs = @()
    $outputs = @()
    
    # Extraire les entrées et sorties depuis le SKILL.md (heuristique simple)
    if ($content -match "Entrées\s*:.*?\n(.*?)(?=\n##|\Z)" -and $matches.Count -gt 1) {
        $inputsBlock = $matches[1]
        foreach ($line in ($inputsBlock -split "`n")) {
            if ($line -match "-\s*(\w+)") {
                $inputs += $matches[1]
            }
        }
    }
    if ($content -match "Sorties\s*:.*?\n(.*?)(?=\n##|\Z)" -and $matches.Count -gt 1) {
        $outputsBlock = $matches[1]
        foreach ($line in ($outputsBlock -split "`n")) {
            if ($line -match "-\s*(\w+)") {
                $outputs += $matches[1]
            }
        }
    }
    
    $skills += [PSCustomObject]@{
        Name    = $d.Name
        Path    = $d.FullName
        Inputs  = $inputs
        Outputs = $outputs
    }
}

# Déduire les Combos (chaîne de compétences compatibles)
$combos = @()
$deadEnds = @()

foreach ($s in $skills) {
    $hasCompatibleOutput = $false
    $hasCompatibleInput = $false
    
    foreach ($t in $skills) {
        if ($s.Name -eq $t.Name) { continue }
        
        # Vérifier si une sortie de s correspond à une entrée de t
        foreach ($out in $s.Outputs) {
            foreach ($inp in $t.Inputs) {
                if ($out -eq $inp) {
                    $hasCompatibleOutput = $true
                    $combos += [PSCustomObject]@{
                        From   = $s.Name
                        To     = $t.Name
                        Via    = $out
                    }
                }
            }
        }
        
        # Vérifier si une sortie de t correspond à une entrée de s
        foreach ($out in $t.Outputs) {
            foreach ($inp in $s.Inputs) {
                if ($out -eq $inp) {
                    $hasCompatibleInput = $true
                }
            }
        }
    }
    
    if ($s.Outputs.Count -gt 0 -and -not $hasCompatibleOutput) {
        $deadEnds += $s.Name
    }
}

$weaveReport = [PSCustomObject]@{
    Timestamp       = $timestamp
    SkillsAnalyzed  = $skills.Count
    CombosDeduced   = $combos.Count
    DeadEnds        = $deadEnds.Count
    Combos          = $combos
    DeadEndList     = $deadEnds
}

$weaveReport | ConvertTo-Json -Depth 3

if ($OutputPath) {
    $weaveReport | ConvertTo-Json -Depth 3 | Out-File -FilePath $OutputPath -Encoding UTF8
}

Write-Wal "[WEAVE] skills=$($skills.Count) combos=$($combos.Count) deadends=$($deadEnds.Count)"

exit 0