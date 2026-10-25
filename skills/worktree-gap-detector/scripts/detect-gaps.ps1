#==============================================================================
# SKILL: worktree-gap-detector
# Rôle: Détecter les worktrees "fuites" et recommander une action.
# Couche CRUD — Read + Alerte
#==============================================================================

[CmdletBinding()]
param(
    [int]$IdleThresholdHours = 24,
    [int]$UnmergedThresholdDays = 3,
    [string]$ProjectFilter = "",
    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\wtg-wal.log"
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

# Récupérer les worktrees via agent_manager
$listOutput = & agent_manager list 2>&1 | Out-String
$worktrees = @()
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
            HasSession  = $true
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
        # Détection de présence de session
        if ($line -notmatch "idle|busy|retry|offline|waiting" -and $line -notmatch "question|permission") {
            $currentWt.HasSession = $false
        }
    }
}
if ($currentWt) { $worktrees += $currentWt }

# Filtrer par projet
if ($ProjectFilter) {
    $worktrees = $worktrees | Where-Object { $_.Name -like "*$ProjectFilter*" }
}

# Détection des fuites
$recommendations = @()
foreach ($wt in $worktrees) {
    $rec = [PSCustomObject]@{
        WorktreeId = $wt.Id
        Name       = $wt.Name
        Branch     = $wt.Branch
        State      = $wt.State
        Action     = ""
        Reason     = ""
    }
    
    # Orphelin (pas de session) depuis > 24h
    if (-not $wt.HasSession) {
        $rec.Action = "crush"
        $rec.Reason = "Worktree sans session depuis > 24h (orphelin)"
    }
    # Idle + branche non mergée
    elseif ($wt.State -eq "idle") {
        $rec.Action = "closeout"
        $rec.Reason = "Worktree idle depuis plus de $IdleThresholdHours heures"
    }
    # ahead > 0, behind = 0 (branche non pushée)
    elseif ($wt.Ahead -gt 0 -and $wt.Behind -eq 0) {
        $rec.Action = "push"
        $rec.Reason = "Branche avec $($wt.Ahead) commit(s) non pushé(s)"
    }
    
    if ($rec.Action) {
        $recommendations += $rec
    }
}

$report = [PSCustomObject]@{
    Timestamp       = $timestamp
    IdleThresholdHours = $IdleThresholdHours
    UnmergedThresholdDays = $UnmergedThresholdDays
    ProjectFilter   = $ProjectFilter
    TotalWorktrees  = $worktrees.Count
    AtRisk          = $recommendations.Count
    Recommendations = $recommendations
}

$report | ConvertTo-Json -Depth 3

Write-Wal "[WTG] detect_gaps project=$ProjectFilter total=$($worktrees.Count) at_risk=$($recommendations.Count)"

exit 0