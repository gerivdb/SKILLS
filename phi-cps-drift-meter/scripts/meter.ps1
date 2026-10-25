# meter.ps1
# phi-cps-drift-meter - Mesure de friction (F) et entropie (H) lors de l'exécution d'un Combo
# Conforme à la règle phi-cps-drift-meter (intent_hash: 0xSKILL_PHI_CPS_DRIFT_METER_20261025)
# Encodage strict CP1252 - Aucun caractère UTF-8 exotique

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ComboId,

    [Parameter(Mandatory = $false)]
    [string]$ExecutionTrace,

    [Parameter(Mandatory = $false)]
    [string]$BaselineMetrics,

    [Parameter(Mandatory = $false)]
    [double]$ExpectedEntropy = 0.0
)

$ErrorActionPreference = "Stop"

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Measure-Friction([string]$trace) {
    $steps = $trace.Split(";") | Where-Object { $_ -ne "" }
    $blocked = ($steps | Where-Object { $_ -match "blocked|freeze|error|timeout" }).Count
    $total = $steps.Count
    if ($total -eq 0) { return 0.0 }
    return [math]::Round($blocked / $total, 4)
}

function Measure-Entropy([string]$trace) {
    $steps = $trace.Split(";") | Where-Object { $_ -ne "" }
    $total = $steps.Count
    if ($total -eq 0) { return 0.0 }
    $groups = $steps | Group-Object
    $entropy = 0.0
    foreach ($group in $groups) {
        $p = $group.Count / $total
        $entropy -= $p * [math]::Log($p, 2)
    }
    return [math]::Round($entropy, 4)
}

# === EXECUTION PRINCIPALE ===
$trace = $ExecutionTrace
if (-not $trace) {
    $trace = "nominal;nominal;completed"
}

$friction = Measure-Friction -trace $trace
$entropy = Measure-Entropy -trace $trace
$driftDetected = $friction -gt 0.5 -or [math]::Abs($entropy - $ExpectedEntropy) -gt 0.5
$driftMagnitude = [math]::Round([math]::Max($friction, [math]::Abs($entropy - $ExpectedEntropy)), 4)

Write-Log "Mesure phi-cps pour Combo $ComboId : F=$friction, H=$entropy, drift=$driftDetected"
Write-Output "friction_score=$friction"
Write-Output "entropy_value=$entropy"
Write-Output "drift_detected=$driftDetected"
Write-Output "drift_magnitude=$driftMagnitude"

if ($driftDetected) {
    Write-Log "Drift détecté pour Combo $ComboId (magnitude=$driftMagnitude)"
    exit 1
}

exit 0
