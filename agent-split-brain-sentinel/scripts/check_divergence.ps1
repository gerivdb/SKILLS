# check_divergence.ps1
# Agent Split-Brain Sentinel - Détecteur de divergence entre branches soeurs
# Conforme à la règle agent-split-brain-sentinel (intent_hash: 0xAGENT_SPLIT_BRAIN_SENTINEL_20261025)

$ErrorActionPreference = "Stop"
$Script:RepoRoot = Resolve-Path "."
$Script:AlertsDir = Join-Path $Script:RepoRoot ".kilo\split_brain_alerts"
$Script:Errors = @()
$Script:Collisions = @()

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Get-DefaultBranch {
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $branch = git symbolic-ref refs/remotes/origin/HEAD 2>$null | ForEach-Object { $_.Split('/') | Select-Object -Last 1 }
    $ErrorActionPreference = $prevEAP
    if (-not $branch) { $branch = "main" }
    return $branch
}

function Get-FeatureBranches([string]$defaultBranch) {
    $output = git branch --no-merged "origin/$defaultBranch" 2>$null
    $branches = @()
    foreach ($line in $output) {
        $trimmed = $line.Trim() -replace '^\*', '' -replace '\s+', ''
        if ($trimmed -and $trimmed -ne $defaultBranch) {
            $branches += $trimmed
        }
    }
    return $branches
}

function Get-ModifiedFiles([string]$branch, [string]$defaultBranch) {
    $output = git diff "$defaultBranch..$branch" --name-only 2>$null
    $files = @()
    foreach ($line in $output) {
        $trimmed = $line.Trim()
        if ($trimmed) { $files += $trimmed }
    }
    return $files
}

function Is-ContractFile([string]$path) {
    $lower = $path.ToLower()
    return $lower -match '\.(json|yaml|yml|ontology|api)$' -or
           $lower -contains 'schema' -or
           $lower -contains 'contract' -or
           $lower -contains 'ontology'
}

function Is-BusinessModule([string]$path) {
    $lower = $path.ToLower()
    return $lower -match '\.(py|zig|js|ts)$' -and
           ($lower -contains 'domain' -or $lower -contains 'module' -or $lower -contains 'service')
}

function Get-SurfaceHash([string[]]$files) {
    $content = ""
    foreach ($file in $files) {
        $fullPath = Join-Path $Script:RepoRoot $file
        if (Test-Path $fullPath) {
            $content += Get-Content -LiteralPath $fullPath -Raw
        }
    }
    if (-not $content) { return "empty" }
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
    $hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
    return [BitConverter]::ToString($hash).Replace("-", "").ToLower()
}

function Write-Alert([string]$branch1, [string]$branch2, [string[]]$conflictingFiles, [string]$severity) {
    if (-not (Test-Path $Script:AlertsDir)) {
        New-Item -ItemType Directory -Path $Script:AlertsDir | Out-Null
    }
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    $alertFile = Join-Path $Script:AlertsDir "collision_$([System.Guid]::NewGuid().ToString('N').Substring(0,8)).json"
    $alert = @{
        alert_type = "EARLY_COLLISION_WARNING"
        branches_involved = @($branch1, $branch2)
        conflicting_files = $conflictingFiles
        timestamp_utc = $timestamp
        severity = $severity
    } | ConvertTo-Json -Depth 10
    Set-Content -LiteralPath $alertFile -Value $alert -Encoding UTF8
    $Script:Collisions += @{
        branches = @($branch1, $branch2)
        files = $conflictingFiles
        severity = $severity
    }
    Write-Log "ALERTE EARLY_COLLISION_WARNING : $branch1 vs $branch2 - $($conflictingFiles.Count) fichier(s) en conflit ($severity)"
}

# === EXÉCUTION PRINCIPALE ===
Write-Log "=== Démarrage du Split-Brain Sentinel ==="

$defaultBranch = Get-DefaultBranch
Write-Log "Branche par défaut : $defaultBranch"

$featureBranches = Get-FeatureBranches -defaultBranch $defaultBranch
Write-Log "$($featureBranches.Count) branche(s) feature active(s) détectée(s)."

if ($featureBranches.Count -lt 2) {
    Write-Log "Moins de 2 branches actives - pas de détection de collision nécessaire."
    Write-Log "branches_active : $($featureBranches.Count)"
    Write-Log "branches_analyzed : 0"
    Write-Log "collisions_detected : 0"
    Write-Log "alerts_generated : 0"
    exit 0
}

# Analyser chaque paire de branches
$branchData = @{}
foreach ($branch in $featureBranches) {
    $files = Get-ModifiedFiles -branch $branch -defaultBranch $defaultBranch
    $branchData[$branch] = $files
}

$contractFilesByBranch = @{}
$moduleFilesByBranch = @{}
foreach ($branch in $featureBranches.Keys) {
    $files = $branchData[$branch]
    $contractFilesByBranch[$branch] = $files | Where-Object { Is-ContractFile $_ }
    $moduleFilesByBranch[$branch] = $files | Where-Object { Is-BusinessModule $_ }
}

$collisionCount = 0
$branches = $featureBranches.Keys
for ($i = 0; $i -lt $branches.Count; $i++) {
    for ($j = $i + 1; $j -lt $branches.Count; $j++) {
        $b1 = $branches[$i]
        $b2 = $branches[$j]

        # Collision sur fichiers de contrat
        $contract1 = @($contractFilesByBranch[$b1])
        $contract2 = @($contractFilesByBranch[$b2])
        $contractConflict = Compare-Object $contract1 $contract2 -IncludeEqual -ExcludeDifferent | Where-Object { $_.SideIndicator -eq '==' } | ForEach-Object { $_.InputObject }

        if ($contractConflict.Count -gt 0) {
            Write-Alert -branch1 $b1 -branch2 $b2 -conflictingFiles $contractConflict -severity "HIGH"
            $collisionCount++
        }

        # Collision sur modules business
        $module1 = @($moduleFilesByBranch[$b1])
        $module2 = @($moduleFilesByBranch[$b2])
        $moduleConflict = Compare-Object $module1 $module2 -IncludeEqual -ExcludeDifferent | Where-Object { $_.SideIndicator -eq '==' } | ForEach-Object { $_.InputObject }

        if ($moduleConflict.Count -gt 0) {
            Write-Alert -branch1 $b1 -branch2 $b2 -conflictingFiles $moduleConflict -severity "MEDIUM"
            $collisionCount++
        }
    }
}

# Rapport final
Write-Log "=== Rapport du Split-Brain Sentinel ==="
Write-Log "branches_active : $($featureBranches.Count)"
Write-Log "branches_analyzed : $($featureBranches.Count)"
Write-Log "collisions_detected : $collisionCount"
Write-Log "alerts_generated : $($Script:Collisions.Count)"
if ($Script:Errors.Count -gt 0) {
    Write-Log "ERREURS :"
    $Script:Errors | ForEach-Object { Write-Log "  - $_" }
    exit 1
}
exit 0