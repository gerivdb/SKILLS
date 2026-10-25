# Script de résolution de dépendances DAG (Combo-Dependency-Resolver)
# Rôle : calcule le graphe de dépendances avant d'exécuter un Combo
# Encodage : CP1252

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$ComboFile,

    [Parameter(Mandatory=$false)]
    [string[]]$Skills,

    [Parameter(Mandatory=$false)]
    [hashtable]$Dependencies = @{}
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$walPath = Join-Path $scriptDir "..\..\WAL\combo\dependency-resolver.wal"

function Write-WalEntry {
    param([string]$ComboId, [int]$SkillsCount, [int]$EdgesCount, [bool]$HasCycle, [string]$OrderJson)
    $ts = (Get-Date).ToUniversalTime().ToString("o")
    $entry = "[COMBO_DAG] comboId=$ComboId skills=$SkillsCount edges=$EdgesCount hasCycle=$HasCycle order=$OrderJson ts=$ts"
    $null = $(New-Item -ItemType File -Path $walPath -Force) | Out-Null
    Add-Content -LiteralPath $walPath -Value $entry -Encoding UTF8
    Write-Output $entry
}

function Load-ComboDefinition {
    param([string]$Path)
    $raw = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    $skillIds = @()
    $deps = @{}
    foreach ($s in $raw.skills) {
        $skillIds += $s.id
        $deps[$s.id] = @($s.dependsOn)
    }
    return @{ skills = $skillIds; dependencies = $deps; comboId = $raw.comboId }
}

function Test-CycleDfs {
    param([string]$Node, [hashtable]$Deps, [hashtable]$Color, [ref]$HasCycle)
    $Color[$Node] = "gray"
    foreach ($dep in $Deps[$Node]) {
        if ($Color.ContainsKey($dep) -and $Color[$dep] -eq "gray") {
            $HasCycle.Value = $true
            return
        }
        if (-not $Color.ContainsKey($dep)) {
            Test-CycleDfs -Node $dep -Deps $Deps -Color $Color -HasCycle $HasCycle
            if ($HasCycle.Value) { return }
        }
    }
    $Color[$Node] = "black"
}

function Resolve-Dag {
    param([string[]]$SkillIds, [hashtable]$Deps, [string]$ComboId)
    $colors = @{}
    $hasCycle = $false
    foreach ($s in $SkillIds) {
        if (-not $colors.ContainsKey($s)) {
            Test-CycleDfs -Node $s -Deps $Deps -Color $colors -HasCycle ([ref]$hasCycle)
        }
    }

    if ($hasCycle) {
        Write-WalEntry -ComboId $ComboId -SkillsCount $SkillIds.Count -EdgesCount 0 -HasCycle $true -OrderJson "null"
        Write-Error "Cycle détecté dans le graphe de dépendances du combo $ComboId. Exécution bloquée."
        exit 3
    }

    # Kahn's algorithm pour tri topologique
    $inDegree = @{}
    foreach ($s in $SkillIds) { $inDegree[$s] = 0 }
    foreach ($s in $SkillIds) {
        foreach ($dep in $Deps[$s]) {
            if ($inDegree.ContainsKey($dep)) { $inDegree[$dep] = 0 } # ensure exists
        }
    }
    foreach ($s in $SkillIds) {
        foreach ($dep in $Deps[$s]) {
            # edge dep -> s
        }
    }

    # Rebuild adjacency for Kahn
    $adj = @{}
    foreach ($s in $SkillIds) { $adj[$s] = @() }
    foreach ($s in $SkillIds) {
        foreach ($dep in $Deps[$s]) {
            $adj[$dep] += $s
        }
    }

    $indeg = @{}
    foreach ($s in $SkillIds) { $indeg[$s] = 0 }
    foreach ($s in $SkillIds) {
        foreach ($dep in $Deps[$s]) {
            $indeg[$s]++
        }
    }

    $queue = @()
    foreach ($s in $SkillIds) {
        if ($indeg[$s] -eq 0) { $queue += $s }
    }

    $order = @()
    while ($queue.Count -gt 0) {
        $n = $queue[0]
        $queue = $queue[1..($queue.Count-1)]
        $order += $n
        foreach ($m in $adj[$n]) {
            $indeg[$m]--
            if ($indeg[$m] -eq 0) { $queue += $m }
        }
    }

    $edgeCount = 0
    foreach ($s in $SkillIds) { $edgeCount += $Deps[$s].Count }

    $orderJson = ($order | ConvertTo-Json -Compress)
    Write-WalEntry -ComboId $ComboId -SkillsCount $SkillIds.Count -EdgesCount $edgeCount -HasCycle $false -OrderJson $orderJson

    return @{ order = $order; edgeCount = $edgeCount }
}

try {
    $comboId = "unknown"
    $skillIds = @()
    $deps = @{}

    if ($ComboFile -and (Test-Path -LiteralPath $ComboFile)) {
        $def = Load-ComboDefinition -Path $ComboFile
        $comboId = $def.comboId
        $skillIds = $def.skills
        $deps = $def.dependencies
    }
    else {
        $skillIds = $Skills
        $deps = $Dependencies
    }

    if ($skillIds.Count -eq 0) {
        Write-Error "Aucun skill à résoudre."
        exit 1
    }

    $result = Resolve-Dag -SkillIds $skillIds -Deps $deps -ComboId $comboId
    Write-Output "[DAG] Ordre d'exécution : $($result.order -join ' ? ')"
    Write-Output "[DAG] $($result.edgeCount) dépendance(s) résolue(s), aucun cycle."
    exit 0
}
catch {
    Write-Error "Échec de la résolution DAG : $($_.Exception.Message)"
    exit 4
}