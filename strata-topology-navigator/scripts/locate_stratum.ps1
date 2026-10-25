# locate_stratum.ps1
# Strata Topology Navigator - Resolution deterministe O(1) des depots gerivdb
# Conforme à la règle strata-topology-navigator (intent_hash: 0xSTRATA_TOPOLOGY_NAVIGATOR_20261025)
# Encodage strict CP1252 - Aucun caractère UTF-8 exotique

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$RepoName,

    [Parameter(Mandatory = $false)]
    [ValidateSet("L0-CANON", "L1-INFRA", "L2-PLATFORM", "L3-CITIZENS", "L4-TOOLS", "L5-ARCHIVE", "L6-WORK")]
    [string]$Stratum
)

$ErrorActionPreference = "Stop"
$Script:ToolsRoot = "D:\DO\WEB\TOOLS"
$Script:Strata = @(
    @{ Name = "L0-CANON"; Path = "D:\DO\WEB\TOOLS\L0-CANON"; Role = "Socle inviolable, SSoT, Gouvernance" },
    @{ Name = "L1-INFRA"; Path = "D:\DO\WEB\TOOLS\L1-INFRA"; Role = "Infrastructure, Clapet BDCP, Gateways" },
    @{ Name = "L2-PLATFORM"; Path = "D:\DO\WEB\TOOLS\L2-PLATFORM"; Role = "Plateforme d'exécution, Runners, Overlays IDE" },
    @{ Name = "L3-CITIZENS"; Path = "D:\DO\WEB\TOOLS\L3-CITIZENS"; Role = "Citoyens autonomes, Daemons, Superviseurs" },
    @{ Name = "L4-TOOLS"; Path = "D:\DO\WEB\TOOLS\L4-TOOLS"; Role = "Outils transversaux, Registres de compétences" },
    @{ Name = "L5-ARCHIVE"; Path = "D:\DO\WEB\TOOLS\L5-ARCHIVE"; Role = "Dépôts patrimoniaux gelés" },
    @{ Name = "L6-WORK"; Path = "D:\DO\WEB\TOOLS\L6-WORK"; Role = "Chantiers temporaires, Espaces scratch" }
)

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Test-RepoInStratum([string]$stratumPath, [string]$repoName) {
    $candidate = Join-Path $stratumPath $repoName
    if (Test-Path -LiteralPath $candidate -PathType Container) {
        return $candidate
    }
    return $null
}

function Resolve-Repo([string]$repoName) {
    foreach ($stratum in $Script:Strata) {
        $found = Test-RepoInStratum -stratumPath $stratum.Path -repoName $repoName
        if ($found) {
            return @{
                repo_name = $repoName
                stratum = $stratum.Name
                role = $stratum.Role
                absolute_path = $found
                found = $true
            }
        }
    }
    # Fallback : niveau 1 seulement sous D:\DO\WEB\TOOLS, sans récursion
    $candidate = Join-Path $Script:ToolsRoot $repoName
    if (Test-Path -LiteralPath $candidate -PathType Container) {
        return @{
            repo_name = $repoName
            stratum = "L_UNKNOWN"
            role = "Racine L4-TOOLS (niveau 1)"
            absolute_path = $candidate
            found = $true
        }
    }
    return @{
        repo_name = $repoName
        stratum = $null
        role = $null
        absolute_path = $null
        found = $false
    }
}

function Resolve-AllInStratum([string]$stratumName) {
    $stratum = $Script:Strata | Where-Object { $_.Name -eq $stratumName }
    if (-not $stratum) {
        Write-Log "Strate inconnue : $stratumName"
        return
    }
    $stratum = $stratum[0]
    $items = Get-ChildItem -LiteralPath $stratum.Path -Directory | Select-Object -ExpandProperty Name
    $results = @()
    foreach ($item in $items) {
        $results += @{
            repo_name = $item
            stratum = $stratum.Name
            role = $stratum.Role
            absolute_path = Join-Path $stratum.Path $item
            found = $true
        }
    }
    $results | ConvertTo-Json -Depth 3
}

# === EXECUTION PRINCIPALE ===
if ($PSBoundParameters.ContainsKey("RepoName")) {
    $result = Resolve-Repo -repoName $RepoName
    $result | ConvertTo-Json -Depth 3
    if (-not $result.found) {
        Write-Log "Depot non trouvé : $RepoName"
        exit 1
    }
    exit 0
}
elseif ($PSBoundParameters.ContainsKey("Stratum")) {
    Resolve-AllInStratum -stratumName $Stratum
    exit 0
}
else {
    Write-Log "Usage: locate_stratum.ps1 -RepoName <nom> | -Stratum <L0-CANON|L1-INFRA|...>"
    exit 1
}