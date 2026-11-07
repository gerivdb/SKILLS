#==============================================================================
# SKILL: ssot-referential-integrity
# Rôle: Audit relationnel des fichiers d'état local (agent-manager.json,
#       metadata.json). Vérification clés étrangères, purge onglets orphelins.
# Couche: Graphe d'État & JSON
#==============================================================================

[CmdletBinding()]
param(
    [string]$StatePath = ".kilo/agent-manager.json",
    [string]$MetadataPath = "",
    [switch]$Purge,
    [string]$BackupDir = ".kilo/backups",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\ssot-referential-integrity\wal\sri-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    if (-not (Test-Path -LiteralPath (Split-Path -Parent $LogPath))) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# Résoudre le chemin absolu du state file
$stateFullPath = Resolve-Path -LiteralPath $StatePath -ErrorAction SilentlyContinue
if (-not $stateFullPath) {
    Write-Output "[SRI] Fichier introuvable : $StatePath"
    Write-WAL "[SRI] ERROR: state file not found: $StatePath"
    exit 1
}

$stateContent = Get-Content -LiteralPath $stateFullPath -Raw -ErrorAction Stop
$state = $stateContent | ConvertFrom-Json -ErrorAction Stop

# 1. Vérifier la clé étrangère activeTarget
$activeTargetValid = $false
$orphanSessions = @()

if ($state.activeTarget -and $state.activeTarget.sessionId) {
    $targetId = $state.activeTarget.sessionId
    if ($state.sessions -and $state.sessions.PSObject.Properties.Name -contains $targetId) {
        $activeTargetValid = $true
    }
    else {
        $orphanSessions += [PSCustomObject]@{
            SessionId = $targetId
            Reason    = "activeTarget pointe vers une session inexistante"
        }
    }
}
else {
    $orphanSessions += [PSCustomObject]@{
        SessionId = $null
        Reason    = "activeTarget.sessionId absent ou null"
    }
}

# 2. Auditer les onglets pending:<uuid> orphelins
$pendingTabs = @()
$purgedTabs = @()

if ($state.tabOrder -and $state.tabOrder.local) {
    foreach ($tab in $state.tabOrder.local) {
        if ($tab -is [string] -and $tab -like "pending:*") {
            $uuid = $tab.Substring("pending:".Length)
            $exists = $false
            if ($state.sessions) {
                foreach ($s in $state.sessions.PSObject.Properties) {
                    if ($s.Value -and $s.Value.id -eq $uuid) {
                        $exists = $true
                        break
                    }
                }
            }
            if (-not $exists) {
                $pendingTabs += $tab
                if ($Purge) {
                    $purgedTabs += $tab
                }
            }
        }
    }
}

# 3. Purge des onglets orphelins (si -Purge)
if ($Purge -and $purgedTabs.Count -gt 0) {
    # Sauvegarde avant modification
    if (-not (Test-Path -LiteralPath $BackupDir)) {
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    }
    $backupFile = Join-Path $BackupDir "agent-manager.$timestamp.bak"
    Copy-Item -LiteralPath $stateFullPath -Destination $backupFile -Force

    # Retirer les tabs purgés
    $newLocal = $state.tabOrder.local | Where-Object { $_ -notin $purgedTabs }
    $state.tabOrder.local = @($newLocal)

    $state | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $stateFullPath -Encoding UTF8
    Write-WAL "[SRI] PURGE tabs=$($purgedTabs -join ',') backup=$backupFile"
}

# 4. Rapport JSON
$report = [PSCustomObject]@{
    Timestamp         = $timestamp
    StateFile         = $stateFullPath
    ActiveTargetValid = $activeTargetValid
    ActiveTargetId    = $state.activeTarget.sessionId
    OrphanSessions    = $orphanSessions
    PendingTabsFound  = $pendingTabs.Count
    PendingTabs       = $pendingTabs
    PurgedTabs        = $purgedTabs
    PurgePerformed    = $Purge
}

$report | ConvertTo-Json -Depth 5

Write-WAL "[SRI] AUDIT file=$stateFullPath activeTarget_valid=$activeTargetValid orphans=$($orphanSessions.Count) pending_tabs=$($pendingTabs.Count)"

exit 0
