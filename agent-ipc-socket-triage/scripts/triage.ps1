#==============================================================================
# SKILL: agent-ipc-socket-triage
# Rôle: Audit connexions TCP locales, détection sockets Half-Open / CLOSE_WAIT,
#       réfutation faux conflits de ports. Couche Réseau & Flux SSE.
#==============================================================================

[CmdletBinding()]
param(
    [int[]]$TargetPorts = @(4096, 61020),
    [switch]$CloseBlocking,
    [int]$IdleTimeoutSeconds = 30,
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\agent-ipc-socket-triage\wal\ist-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$results = @()

function Write-WAL {
    param([string]$Message)
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $LogPath))) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# 1. Récupérer toutes les connexions TCP locales
$connections = Get-NetTCPConnection -ErrorAction SilentlyContinue |
    Where-Object { $_.LocalAddress -like "127.0.0.1" -or $_.LocalAddress -like "::1" } |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess, CreationTime

if (-not $connections) {
    Write-Output "[IST] Aucune connexion TCP locale trouvée"
    Write-WAL "[IST] ERROR: Get-NetTCPConnection returned nothing"
    exit 1
}

# 2. Filtrer par ports cibles
$filtered = $connections | Where-Object { $TargetPorts -contains $_.LocalPort }

# 3. Détecter les états bloquants
$blockingStates = @("CloseWait", "TimeWait")
$blocking = $filtered | Where-Object { $blockingStates -contains $_.State }

# Détection Half-Open (état intermédiaire sans trafic) — approx par état non établi et non fermé
$halfOpen = $filtered | Where-Object {
    $_.State -notin @("Established", "Closed", "Listen", "Bound") -and
    $_.State -notin $blockingStates
}

# 4. Détecter absence de trafic inter-chunks (connexions Established trop anciennes)
$staleEstablished = $filtered | Where-Object {
    $_.State -eq "Established" -and
    ((Get-Date) - $_.CreationTime).TotalSeconds -gt $IdleTimeoutSeconds
}

# 5. Résoudre les noms de processus pour les sockets bloquantes
$blockingDetails = @()
foreach ($b in $blocking) {
    try {
        $proc = Get-Process -Id $b.OwningProcess -ErrorAction Stop
        $procName = $proc.ProcessName
    }
    catch {
        $procName = "inconnu (PID $($b.OwningProcess))"
    }
    $blockingDetails += [PSCustomObject]@{
        LocalPort     = $b.LocalPort
        RemotePort    = $b.RemotePort
        State         = $b.State
        OwningProcess = $b.OwningProcess
        ProcessName   = $procName
        CreationTime  = $b.CreationTime
        AgeSeconds    = [math]::Round(((Get-Date) - $b.CreationTime).TotalSeconds, 1)
    }
}

# 6. Fermeture forcée des sockets bloquantes (si -CloseBlocking)
if ($CloseBlocking) {
    $closed = @()
    foreach ($b in $blockingDetails) {
        try {
            $proc = Get-Process -Id $b.OwningProcess -ErrorAction Stop
            $proc.CloseMainWindow()
            Start-Sleep -Seconds 2
            if (-not $proc.HasExited) {
                $proc.Kill()
            }
            $closed += $b.OwningProcess
            Write-WAL "[IST] CLOSE pid=$($b.OwningProcess) proc=$($procName) port=$($b.LocalPort) state=$($b.State) status=OK"
        }
        catch {
            Write-WAL "[IST] CLOSE pid=$($b.OwningProcess) proc=$($procName) port=$($b.LocalPort) state=$($b.State) status=FAIL error=$($_.Exception.Message)"
        }
    }
    Write-Output "`n[IST] Processus fermés : $($closed -join ', ')"
}

# 7. Rapport JSON
$report = [PSCustomObject]@{
    Timestamp            = $timestamp
    TotalLocalConnections= $connections.Count
    TargetPortConnections= $filtered.Count
    BlockingSockets      = $blocking.Count
    HalfOpenSockets      = $halfOpen.Count
    StaleEstablished     = $staleEstablished.Count
    BlockingDetails      = $blockingDetails
    FalseConflictRuledOut = ($filtered | Where-Object { $_.State -eq "Listen" }).Count -gt 0
}

$report | ConvertTo-Json -Depth 5

Write-WAL "[IST] AUDIT timestamp=$timestamp ports=$($TargetPorts -join ',') connections=$($filtered.Count) blocking=$($blocking.Count)"

exit 0
