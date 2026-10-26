#==============================================================================
# SKILL: git-merge-safety-gate
# Rôle: Remplacer les hésitations manuelles par un test déterministe.
# Exécute `git branch --merged main`. Si mergée ➔ recommande le skill agent-worktree-pruner.
# Couche CRUD — Read + Décision.
#==============================================================================

[CmdletBinding()]
param(
    [string]$BranchName,      # Nom de la branche à vérifier (obligatoire)
    [string]$RepoPath,        # Chemin du dépôt git (optionnel, défaut : répertoire courant)
    [string]$BaseBranch = "main"  # Branche de référence (défaut : main)
)

$ErrorActionPreference = "Continue"
$timestamp = (Get-Date).ToUniversalTime().ToString("o")

# ── Déterminer le chemin du dépôt ──
if (-not $RepoPath) {
    $RepoPath = (Get-Location).Path
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoPath ".git"))) {
    Write-Output "[FAIL] Aucun dépôt Git trouvé à $RepoPath"
    exit 2
}

# ── Vérifier que la branche existe ──
$branchExists = & git -C $RepoPath branch --list $BranchName 2>&1 | Out-String
if (-not $branchExists) {
    Write-Output "[FAIL] Branche '$BranchName' introuvable dans le dépôt."
    exit 2
}

# ── Test déterministe : git branch --merged main ──
$mergedOutput = & git -C $RepoPath branch --merged $BaseBranch 2>&1 | Out-String

$isMerged = $false
foreach ($line in $mergedOutput -split "`n") {
    $trimmed = $line.Trim()
    # Retirer le marqueur '*' de la branche courante
    $branchOnly = $trimmed.TrimStart("* ").Trim()
    if ($branchOnly -eq $BranchName) {
        $isMerged = $true
        break
    }
}

# ── Rapport ──
$result = [PSCustomObject]@{
    Timestamp       = $timestamp
    BranchName      = $BranchName
    BaseBranch      = $BaseBranch
    IsMerged        = $isMerged
    MergedInto      = if ($isMerged) { $BaseBranch } else { $null }
    Recommendation  = if ($isMerged) { "prune" } else { "keep" }
    SkillRecommande = if ($isMerged) { "agent-worktree-pruner" } else { $null }
}

$jsonResult = $result | ConvertTo-Json -Depth 3
Write-Output $jsonResult

if ($isMerged) {
    Write-Output ""
    Write-Output "[OK] Branche '$BranchName' est mergée dans $BaseBranch."
    Write-Output "[REC] Recommande d'utiliser le skill agent-worktree-pruner pour nettoyer le worktree physique et agent-manager.json."
    exit 0
} else {
    Write-Output ""
    Write-Output "[INFO] Branche '$BranchName' n'est PAS mergée dans $BaseBranch."
    Write-Output "[REC] Conserver la branche. Investiguer pourquoi elle n'est pas encore mergée."
    exit 1
}