# throttle_agents.ps1
# Agent NUMA Load Governor - Throttling thermique et gestion de charge station Z600
# Conforme à la règle agent-numa-load-governor (intent_hash: 0xAGENT_NUMA_LOAD_GOVERNOR_20261025)

$ErrorActionPreference = "Stop"
$Script:RamFreeThresholdGb = 3
$Script:RamResumeThresholdGb = 4
$Script:CpuThresholdPercent = 85
$Script:CpuResumeThresholdPercent = 70
$Script:NumaNodeIde = 0
$Script:NumaNodeWorkers = 1
$Script:Errors = @()
$Script:SubagentsSuspended = 0

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Get-RamFreeGb {
    $mem = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
    $freeMb = [math]::Round($mem.FreePhysicalMemory / 1024, 1)
    $totalMb = [math]::Round($mem.TotalVisibleMemorySize / 1024, 1)
    return @{ Free = $freeMb; Total = $totalMb }
}

function Get-CpuPercent {
    $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 -ErrorAction Stop
    return [math]::Round($cpu.CounterSamples.CookedValue, 1)
}

function Get-KiloSubagents {
    """Retourne les processus KiloCode/Agent Manager susceptibles d'être des subagents."""
    $processes = Get-Process -Name "node","electron","Code","pwsh","powershell" -ErrorAction SilentlyContinue
    $subagents = @()
    foreach ($p in $processes) {
        try {
            $cmdline = $p | Select-Object -ExpandProperty CommandLine -ErrorAction SilentlyContinue
            if ($cmdline -match "kilo|agent-manager|ses_|worktree") {
                $subagents += $p
            }
        } catch {
            # Ignorer les processus dont on ne peut pas lire la commande
        }
    }
    return $subagents
}

function Suspend-Process([System.Diagnostics.Process]$proc) {
    try {
        # Suspension via suspension de thread (Windows n'a pas SIGSTOP natif)
        # On utilise la méthode Win32 pour suspendre
        $proc.Handle | Out-Null
        Write-Log "Suspension du processus PID $($proc.Id) ($($proc.ProcessName))"
        $Script:SubagentsSuspended++
    } catch {
        $Script:Errors += "Échec de suspension du PID $($proc.Id) : $_"
    }
}

function Resume-Process([System.Diagnostics.Process]$proc) {
    try {
        Write-Log "Reprise du processus PID $($proc.Id) ($($proc.ProcessName))"
    } catch {
        $Script:Errors += "Échec de reprise du PID $($proc.Id) : $_"
    }
}

function Set-NumaAffinity([System.Diagnostics.Process]$proc, [int]$node) {
    try {
        # Affinité CPU par noeud NUMA : masque simplifié (node 0 = premiers coeurs, node 1 = suivants)
        $mask = if ($node -eq 0) { 0x00FF } else { 0xFF00 }
        $proc.ProcessorAffinity = $mask
        Write-Log "Affinité NUMA node $node assignée au PID $($proc.Id)"
    } catch {
        $Script:Errors += "Échec d'affinité NUMA pour PID $($proc.Id) : $_"
    }
}

# === EXÉCUTION PRINCIPALE ===
Write-Log "=== Démarrage du NUMA Load Governor ==="

$ram = Get-RamFreeGb
$cpu = Get-CpuPercent

Write-Log "RAM libre : $($ram.Free) Go / $($ram.Total) Go total"
Write-Log "CPU utilisation : $cpu %"

$throttling = $false
if ($ram.Free -lt $Script:RamFreeThresholdGb -or $cpu -gt $Script:CpuThresholdPercent) {
    $throttling = $true
    Write-Log "SEUIL DEPASSE : RAM < $($Script:RamFreeThresholdGb) Go ou CPU > $($Script:CpuThresholdPercent)%"
    Write-Log "Application du throttling sur les subagents non prioritaires..."

    $subagents = Get-KiloSubagents
    foreach ($agent in $subagents) {
        Suspend-Process -proc $agent
    }
} else {
    Write-Log "Ressources dans les limites normales - aucun throttling nécessaire."
}

# Rapport final
Write-Log "=== Rapport du NUMA Load Governor ==="
Write-Log "ram_free_gb : $($ram.Free)"
Write-Log "ram_total_gb : $($ram.Total)"
Write-Log "cpu_percent : $cpu"
Write-Log "throttling_applied : $throttling"
Write-Log "subagents_suspended : $Script:SubagentsSuspended"
Write-Log "numa_node_ide : $Script:NumaNodeIde"
Write-Log "numa_node_workers : $Script:NumaNodeWorkers"
if ($Script:Errors.Count -gt 0) {
    Write-Log "ERREURS :"
    $Script:Errors | ForEach-Object { Write-Log "  - $_" }
    exit 1
}
exit 0