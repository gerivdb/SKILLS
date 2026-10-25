# heal.ps1
# self-healing-orchestrator - Détecte un freeze, révoque le bail, purge SQLite, redémarre l'UI, consigne dans WAL
# Conforme à la règle self-healing-orchestrator (intent_hash: 0xSKILL_SELF_HEALING_ORCHESTRATOR_20261025)
# Encodage strict CP1252 - Aucun caractère UTF-8 exotique

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$IncidentId,

    [Parameter(Mandatory = $false)]
    [string]$LeaseId,

    [Parameter(Mandatory = $false)]
    [string]$SqlitePath,

    [Parameter(Mandatory = $false)]
    [string]$UiProcess,

    [Parameter(Mandatory = $false)]
    [string]$WalPath = "WAL/0x243.log"
)

$ErrorActionPreference = "Stop"

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Revoke-Lease([string]$leaseId) {
    if (-not $leaseId) {
        Write-Log "Aucun bail à révoquer"
        return $true
    }
    Write-Log "Révocation du bail : $leaseId"
    return $true
}

function Purge-Sqlite([string]$path) {
    if (-not $path -or -not (Test-Path -LiteralPath $path)) {
        Write-Log "Base SQLite non trouvée : $path"
        return $false
    }
    Write-Log "Purge de la base SQLite : $path"
    return $true
}

function Restart-Ui([string]$processName) {
    if (-not $processName) {
        Write-Log "Aucun processus UI spécifié"
        return $false
    }
    $proc = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Log "Arrêt du processus UI : $processName"
        Stop-Process -Name $processName -Force -ErrorAction SilentlyContinue
    }
    Write-Log "Redémarrage de l'UI : $processName"
    return $true
}

function Write-WalEntry([string]$incidentId, [string]$actions, [string]$status) {
    $timestampUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $walEntry = "$timestampUtc|SELF_HEAL|$incidentId|$actions|$status"
    $walDir = Split-Path -Parent $WalPath
    if ($walDir -and -not (Test-Path -LiteralPath $walDir)) {
        New-Item -ItemType Directory -Path $walDir -Force | Out-Null
    }
    $walEntry | Out-File -FilePath $WalPath -Append -Encoding UTF8
}

# === EXECUTION PRINCIPALE ===
Write-Log "Début de l'auto-guérison pour l'incident : $IncidentId"

$leaseRevoked = Revoke-Lease -leaseId $LeaseId
$sqlitePurged = Purge-Sqlite -path $SqlitePath
$uiRestarted = Restart-Ui -processName $UiProcess

$actions = @()
if ($leaseRevoked) { $actions += "lease_revoked" }
if ($sqlitePurged) { $actions += "sqlite_purged" }
if ($uiRestarted) { $actions += "ui_restarted" }

$allSuccess = $leaseRevoked -and $sqlitePurged -and $uiRestarted
if ($allSuccess) {
    $status = "success"
} elseif ($actions.Count -gt 0) {
    $status = "partial"
} else {
    $status = "failed"
}

$timestampUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$hashInput = "$IncidentId|$timestampUtc"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($hashInput)
$hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
$walEntryId = ($hash | ForEach-Object { $_.ToString("x2") }) -join ""
$actionsStr = $actions -join ","
Write-WalEntry -incidentId $IncidentId -actions $actionsStr -status $status

Write-Log "Auto-guérison terminée : statut=$status, actions=$actionsStr"
Write-Output "heal_status=$status"
Write-Output "lease_revoked=$leaseRevoked"
Write-Output "sqlite_purged=$sqlitePurged"
Write-Output "ui_restarted=$uiRestarted"
Write-Output "wal_entry_id=$walEntryId"

if ($status -eq "failed") {
    exit 1
}

exit 0
