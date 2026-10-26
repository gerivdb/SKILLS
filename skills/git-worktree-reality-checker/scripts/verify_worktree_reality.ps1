#==============================================================================
# SKILL: git-worktree-reality-checker
# Rôle: Interdire d'affirmer qu'un worktree "n'existe pas" sur un simple appel CLI négatif.
# Vérifie simultanément : dossier physique, déclaration Git, présence dans agent-manager.json.
# Couche CRUD — Read + Vérification (règle de la double preuve).
#==============================================================================

[CmdletBinding()]
param(
    [string]$WorktreePath,       # Chemin du worktree à vérifier (obligatoire)
    [string]$WorktreeId,         # ID du worktree dans agent-manager.json (optionnel)
    [string]$ProjectId = "SKILLS", # RAGX ou SKILLS (défaut SKILLS)
    [string]$AgentManagerJson = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\.kilo\agent-manager.json"
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

# Résultat final
$result = [PSCustomObject]@{
    WorktreePath   = $WorktreePath
    WorktreeId     = $WorktreeId
    Timestamp      = $timestamp
    Exists         = $false
    Sources        = @()
    ConfirmedBy    = @()
    TreatAsExisting = $false
}

# ── Source 1 : Dossier physique ──
$physicalExists = $false
if ($WorktreePath) {
    if (Test-Path -LiteralPath $WorktreePath) {
        $physicalExists = $true
        $result.Sources += "dossier_physique"
        $result.ConfirmedBy += "dossier_physique"
        Write-Output "[INFO] Dossier physique trouvé : $WorktreePath"
    } else {
        Write-Output "[INFO] Dossier physique absent : $WorktreePath"
    }
}

# ── Source 2 : Déclaration Git (git worktree list) ──
$gitDeclared = $false
if ($WorktreePath) {
    # Déterminer la racine du dépôt à partir du chemin du worktree
    $repoRoot = Split-Path -Parent $WorktreePath
    # Remonter jusqu'à trouver un .git
    $probe = $repoRoot
    while ($probe -and $probe -ne (Split-Path $probe)) {
        if (Test-Path -LiteralPath (Join-Path $probe ".git")) {
            $repoRoot = $probe
            break
        }
        $probe = Split-Path -Parent $probe
    }

    if (Test-Path -LiteralPath (Join-Path $repoRoot ".git")) {
        $wtList = & git -C $repoRoot worktree list 2>&1 | Out-String
        if ($wtList -match [regex]::Escape($WorktreePath)) {
            $gitDeclared = $true
            $result.Sources += "declare_git"
            $result.ConfirmedBy += "declare_git"
            Write-Output "[INFO] Worktree déclaré dans Git : $WorktreePath"
        } else {
            Write-Output "[INFO] Worktree non déclaré dans Git : $WorktreePath"
        }
    } else {
        Write-Output "[WARN] Aucun dépôt Git trouvé à partir de $WorktreePath"
    }
}

# ── Source 3 : Présence dans agent-manager.json ──
$jsonDeclared = $false
if (Test-Path -LiteralPath $AgentManagerJson) {
    $jsonContent = Get-Content -LiteralPath $AgentManagerJson -Raw -ErrorAction SilentlyContinue
    if ($jsonContent) {
        try {
            $json = $jsonContent | ConvertFrom-Json
            # Recherche par ID
            if ($WorktreeId -and $json.worktrees -and $json.worktrees.PSObject.Properties.Name -contains $WorktreeId) {
                $jsonDeclared = $true
                $result.Sources += "agent_manager_json"
                $result.ConfirmedBy += "agent_manager_json"
                Write-Output "[INFO] Worktree ID $WorktreeId trouvé dans agent-manager.json"
            }
            # Recherche par path dans les worktrees
            if (-not $jsonDeclared -and $WorktreePath -and $json.worktrees) {
                foreach ($wtId in $json.worktrees.PSObject.Properties.Name) {
                    $wt = $json.worktrees.$wtId
                    if ($wt.path -eq $WorktreePath) {
                        $jsonDeclared = $true
                        $result.Sources += "agent_manager_json"
                        $result.ConfirmedBy += "agent_manager_json"
                        if (-not $WorktreeId) { $result.WorktreeId = $wtId }
                        Write-Output "[INFO] Chemin $WorktreePath trouvé dans agent-manager.json (ID: $wtId)"
                        break
                    }
                }
            }
        } catch {
            Write-Output "[WARN] Impossible de parser agent-manager.json : $($_.Exception.Message)"
        }
    }
} else {
    Write-Output "[WARN] agent-manager.json introuvable : $AgentManagerJson"
}

# ── Décision finale (règle de la double preuve) ──
$result.Exists = $physicalExists -or $gitDeclared -or $jsonDeclared
$result.TreatAsExisting = $result.Exists

if ($result.Exists) {
    Write-Output "[OK] Worktree CONFIRMÉ existant (sources : $($result.Sources -join ', '))"
    $result | ConvertTo-Json -Depth 3
    exit 0
} else {
    Write-Output "[FAIL] Worktree non confirmé par aucune source de vérité. Ne pas affirmer 'n'existe pas' sans vérification complémentaire."
    $result | ConvertTo-Json -Depth 3
    exit 3  # Code 3 = non confirmé (distinct de 1=erreur, 2=conflit)
}