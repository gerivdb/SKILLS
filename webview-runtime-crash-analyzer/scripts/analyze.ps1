#==============================================================================
# SKILL: webview-runtime-crash-analyzer
# Rôle: Corrélation état manquant ↔ plantage arbre composants React Webview.
#       Détection exceptions "Cannot read properties of undefined".
#       Prescription état neutre de repli. Couche Rendu React & ErrorBoundary.
#==============================================================================

[CmdletBinding()]
param(
    [string]$WebviewLogPath = "",
    [string]$StatePath = ".kilo/agent-manager.json",
    [switch]$PrescribeFallback,
    [string]$FallbackPath = ".kilo/fallback-state.json",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\webview-runtime-crash-analyzer\wal\wca-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$exceptions = @()

function Write-WAL {
    param([string]$Message)
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $LogPath))) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# 1. Scanner les logs webview pour les exceptions React
if ($WebviewLogPath -and (Test-Path -LiteralPath $WebviewLogPath)) {
    $logContent = Get-Content -LiteralPath $WebviewLogPath -Raw -ErrorAction SilentlyContinue
    if ($logContent) {
        # Recherche des exceptions "Cannot read properties of undefined"
        $matches = [regex]::Matches($logContent, "Cannot read properties of ([^\s]+) \(reading '([^']+)'\)", [System.Text.RegularExpressions.RegexOptions]::Multiline)
        foreach ($m in $matches) {
            $exceptions += [PSCustomObject]@{
                ObjectType = $m.Groups[1].Value
                Property   = $m.Groups[2].Value
                FullMatch  = $m.Value
            }
        }
    }
}

# 2. Vérifier l'état agent
$agentStateValid = $false
$agentState = $null
if (Test-Path -LiteralPath $StatePath) {
    try {
        $agentState = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json -ErrorAction Stop
        $agentStateValid = $true
    }
    catch {
        $agentStateValid = $false
    }
}

# 3. Déterminer si le DOM d'input est démonté (heuristique basé sur les exceptions + état)
$componentDemounted = $exceptions.Count -gt 0

# 4. Générer l'état neutre de repli
$fallbackState = [PSCustomObject]@{
    sessions        = @{}
    activeTarget    = $null
    tabOrder        = [PSCustomObject]@{ local = @() }
    version         = "1.0.0-fallback"
    generatedAt     = $timestamp
    reason          = "webview-runtime-crash-analyzer fallback state"
}

# 5. Appliquer l'état neutre si demandé
$fallbackApplied = $false
if ($PrescribeFallback) {
    try {
        if (-not (Test-Path -LiteralPath (Split-Path -Parent $FallbackPath))) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $FallbackPath) | Out-Null
        }
        $fallbackState | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $FallbackPath -Encoding UTF8
        $fallbackApplied = $true
        Write-WAL "[WCA] FALLBACK_PRESCRIBED path=$FallbackPath exceptions=$($exceptions.Count)"
    }
    catch {
        Write-WAL "[WCA] FALLBACK_PRESCRIBED path=$FallbackPath status=FAIL error=$($_.Exception.Message)"
    }
}

# 6. Rapport JSON
$report = [PSCustomObject]@{
    Timestamp          = $timestamp
    WebviewLogPath     = $WebviewLogPath
    ExceptionsDetected = $exceptions.Count
    Exceptions         = $exceptions
    AgentStateValid    = $agentStateValid
    ComponentDemounted = $componentDemounted
    FallbackPrescribed = $fallbackApplied
    FallbackPath       = $FallbackPath
    FallbackState      = $fallbackState
}

$report | ConvertTo-Json -Depth 5

Write-Wal "[WCA] ANALYZE log=$WebviewLogPath exceptions=$($exceptions.Count) agent_valid=$agentStateValid demounted=$componentDemounted fallback=$fallbackApplied"

exit 0
