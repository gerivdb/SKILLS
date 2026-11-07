#==============================================================================
# SKILL: agent-process-forensics
# Rôle: Cartographie arbre de processus, détection daemons orphelins, élimination zombies.
# Couche: OS & Arborescence
#==============================================================================

[CmdletBinding()]
param(
    [switch]$Eliminate,
    [int]$MaxAgeMinutes = 30,
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\agent-process-forensics\wal\apf-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$results = @()

# Fonction d'écriture WAL
function Write-WAL {
    param([string]$Message)
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $LogPath))) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# 1. Récupérer tous les processus via CIM/WMI
$processes = Get-CimInstance -ClassName Win32_Process -ErrorAction SilentlyContinue |
    Select-Object ProcessId, ParentProcessId, Name, CommandLine, CreationDate

if (-not $processes) {
    Write-Output "[APF] Échec de récupération des processus via CIM/WMI"
    Write-WAL "[APF] ERROR: Get-CimInstance Win32_Process returned nothing"
    exit 1
}

# Construire un dictionnaire parent -> enfants
$parentMap = @{}
foreach ($p in $processes) {
    $ppid = $p.ParentProcessId
    if (-not $parentMap.ContainsKey($ppid)) {
        $parentMap[$ppid] = @()
    }
    $parentMap[$ppid] += $p.ProcessId
}

# 2. Filtrer les cibles prioritaires
$targets = $processes | Where-Object {
    $_.Name -in @("kilo.exe", "node.exe", "pwsh.exe", "powershell.exe") -or
    ($_.CommandLine -like "*kilo*") -or
    ($_.CommandLine -like "*vscode-webview*")
}

# 3. Détecter les zombies
$now = (Get-Date).ToUniversalTime()
$zombies = @()

foreach ($p in $targets) {
    $ageMinutes = ($now - $p.CreationDate).TotalMinutes
    $isOrphan = ($p.ParentProcessId -eq 1)
    $isStale = ($ageMinutes -gt $MaxAgeMinutes)
    $isKiloNoWindow = ($_.Name -eq "kilo.exe")

    $reason = @()
    if ($isOrphan) { $reason += "ParentPID=1 (orphelin)" }
    if ($isStale)  { $reason += "Âge > $MaxAgeMinutes min" }
    if ($isKiloNoWindow) { $reason += "kilo.exe sans fenêtre principale" }

    if ($reason.Count -gt 0) {
        $zombies += [PSCustomObject]@{
            ProcessId   = $p.ProcessId
            ParentPID   = $p.ParentProcessId
            Name        = $p.Name
            CommandLine = $p.CommandLine
            CreationDate= $p.CreationDate
            AgeMinutes  = [math]::Round($ageMinutes, 1)
            Reason      = $reason -join "; "
        }
    }
}

# 4. Afficher le rapport
$report = [PSCustomObject]@{
    Timestamp     = $timestamp
    TotalProcesses= $processes.Count
    TargetsFound  = $targets.Count
    ZombiesDetected = $zombies.Count
    Zombies       = $zombies
}

$report | ConvertTo-Json -Depth 5

# 5. Élimination (si -Eliminate)
if ($Eliminate) {
    $eliminated = @()
    foreach ($z in $zombies) {
        try {
            $proc = Get-Process -Id $z.ProcessId -ErrorAction Stop
            # Tentative arrêt gracieux
            $proc.CloseMainWindow()
            Start-Sleep -Seconds 2
            if (-not $proc.HasExited) {
                $proc.Kill()
                $proc.WaitForExit(5000)
            }
            $eliminated += $z.ProcessId
            Write-WAL "[APF] ELIMINATE pid=$($z.ProcessId) name=$($z.Name) reason=$($z.Reason) status=OK"
        }
        catch {
            Write-WAL "[APF] ELIMINATE pid=$($z.ProcessId) name=$($z.Name) reason=$($z.Reason) status=FAIL error=$($_.Exception.Message)"
        }
    }
    Write-Output "`n[APF] PID éliminés : $($eliminated -join ', ')"
}

Write-WAL "[APF] SCAN timestamp=$timestamp zombies_detected=$($zombies.Count)"

exit 0
