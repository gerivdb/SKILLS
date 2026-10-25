# notarize.ps1
# wal-event-notary - Notarisation des transitions d'état dans WAL/0x243.log
# Conforme à la règle wal-event-notary (intent_hash: 0xSKILL_WAL_EVENT_NOTARY_20261025)
# Encodage strict CP1252 - Aucun caractère UTF-8 exotique

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CitizenId,

    [Parameter(Mandatory = $true)]
    [string]$FromState,

    [Parameter(Mandatory = $true)]
    [string]$ToState,

    [Parameter(Mandatory = $false)]
    [string]$ComboId,

    [Parameter(Mandatory = $false)]
    [string]$WalPath = "WAL/0x243.log"
)

$ErrorActionPreference = "Stop"

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function New-WalEntryId([string]$citizenId, [string]$fromState, [string]$toState, [string]$timestamp) {
    $content = "$citizenId|$fromState|$toState|$timestamp"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
    $hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
    return ($hash | ForEach-Object { $_.ToString("x2") }) -join ""
}

# === EXECUTION PRINCIPALE ===
$timestampUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$walEntryId = New-WalEntryId -citizenId $CitizenId -fromState $FromState -toState $ToState -timestamp $timestampUtc

# Construire l'entrée WAL
$walEntry = "$timestampUtc|$CitizenId|$FromState|$ToState|$ComboId|$walEntryId"

# Assurer l'existence du répertoire WAL
$walDir = Split-Path -Parent $WalPath
if ($walDir -and -not (Test-Path -LiteralPath $walDir)) {
    New-Item -ItemType Directory -Path $walDir -Force | Out-Null
}

# Append de l'entrée (mode append-only)
$walEntry | Out-File -FilePath $WalPath -Append -Encoding UTF8

Write-Log "Entrée WAL notarisée : $walEntryId pour Citizen $CitizenId ($FromState -> $ToState)"
Write-Output "wal_entry_id=$walEntryId"
Write-Output "wal_path=$WalPath"
Write-Output "confirmed=True"

exit 0
