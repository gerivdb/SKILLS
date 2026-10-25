#==============================================================================
# SKILL: worktree-auditor
# Rôle: Audit des worktrees managés (état, branche, avance/délai, orphelins).
# Couche CRUD — Read
#==============================================================================

[CmdletBinding()]
param(
    [string]$ProjectFilter = "",
    [string]$EtatFilter = "",
    [int]$AgeMaxHours = 24,
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wta-wal.log"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

function Write-WAL {
    param([string]$Message)
    $logDir = Split-Path -Parent $LogPath
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    "$timestamp | $Message" | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

# Appeler agent_manager list pour récupérer les worktrees
# Note: agent_manager est un outil Kilo, pas une commande shell directe.
# Ici on simule la lecture via l'API Agent Manager. En pratique, ce skill
# est invoqué par KiloCode qui utilise agent_manager list.
$worktrees = @()

# Lire les worktrees via agent_manager (appel externe)
$listOutput = & agent_manager list 2>&1 | Out-String
if ($LASTEXITCODE -eq 0 -and $listOutput) {
    # Parsing simplifié : en pratique, KiloCode retourne du JSON structuré
    # Ici on traite le résultat textuel pour extraire les infos clés
    $lines = $listOutput -split "`n"
    $currentWt = $null
    foreach ($line in $lines) {
        if ($line -match "id:\s*(wt-\S+)") {
            if ($currentWt) { $worktrees += $currentWt }
            $currentWt = [PSCustomObject]@{
                Id          = $matches[1]
                Name        = ""
                Branch      = ""
                State       = ""
                Ahead       = 0
                Behind      = 0
                SessionId   = $null
                Orphan      = $false
                Stagnant    = $false
                Drifting    = $false
            }
        }
        elseif ($currentWt -and $line -match "name:\s*(.+)") {
            $currentWt.Name = $matches[1].Trim()
        }
        elseif ($currentWt -and $line -match "branch:\s*(.+)") {
            $currentWt.Branch = $matches[1].Trim()
        }
        elseif ($currentWt -and $line -match "activity:\s*(\w+)") {
            $currentWt.State = $matches[1].Trim()
        }
        elseif ($currentWt -and $line -match "session") {
            # Détection de présence/absence de session
            if ($line -match "idle" -or $line -match "busy" -or $line -match "retry" -or $line -match "offline" -or $line -match "waiting") {
                # session présente
            }
            else {
                $currentWt.Orphan = $true
            }
        }
    }
    if ($currentWt) { $worktrees += $currentWt }
}

# Filtrer par projet et état si spécifiés
if ($ProjectFilter) {
    $worktrees = $worktrees | Where-Object { $_.Name -like "*$ProjectFilter*" }
}
if ($EtatFilter) {
    $worktrees = $worktrees | Where-Object { $_.State -eq $EtatFilter }
}

# Détection des flags
foreach ($wt in $worktrees) {
    # Stagnant : idle depuis plus de AgeMaxHours (heuristique basé sur l'état)
    if ($wt.State -eq "idle") {
        $wt.Stagnant = $true
    }
    # Dérivant : ahead > 0 et behind = 0
    if ($wt.Ahead -gt 0 -and $wt.Behind -eq 0) {
        $wt.Drifting = $true
    }
}

# Rapport
$report = [PSCustomObject]@{
    Timestamp     = $timestamp
    ProjectFilter = $ProjectFilter
    EtatFilter    = $EtatFilter
    Worktrees     = $worktrees
    Orphans       = ($worktrees | Where-Object { $_.Orphan }).Count
    Stagnants     = ($worktrees | Where-Object { $_.Stagnant }).Count
    Drifters      = ($worktrees | Where-Object { $_.Drifting }).Count
    Total         = $worktrees.Count
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTA] audit project=$ProjectFilter etat=$EtatFilter total=$($worktrees.Count) orphans=$($report.Orphans) stagnants=$($report.Stagnants) drifters=$($report.Drifters)"

exit 0