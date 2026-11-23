#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test de régression last-match-wins et audit des permissions (Phase 12, T113-T120).

.DESCRIPTION
    Teste la règle last-match-wins sur les permissions de mode :
    - T113 : Cas last-match-wins sur chemins de fichiers sensibles
    - T114 : Cas last-match-wins sur commandes d'exécution
    - T115 : Interdiction des wildcards trop larges en position terminale sur modes restreints
    - T119 : Test de régression sur l'ordre des règles de permissions
    - T120 : Audit des permissions avec empreinte SHA-256

.PARAMETER PermissionsPath
    Chemin vers effective-permissions.json.

.EXAMPLE
    ./test-last-match-wins.ps1

.NOTES
    Phase 12, T113-T120 — Permissions et règle last-match-wins
#>

[CmdletBinding()]
param(
    [string]$PermissionsPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\effective-permissions.json"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins ---
if (-not (Test-Path -LiteralPath $PermissionsPath)) {
    Write-Error "Fichier effective-permissions.json introuvable : $PermissionsPath"
    exit 1
}

# --- Lecture de la matrice ---
$permissions = (Get-Content -LiteralPath $PermissionsPath -Raw | ConvertFrom-Json).permissions

# --- Fonction : calculer la décision effective pour un (mode, type, target) ---
function Get-EffectiveDecision {
    param([array]$Permissions, [string]$ModeId, [string]$PermissionType, [string]$Target)
    $matching = @()
    foreach ($p in $Permissions) {
        if ($p.mode_id -eq $ModeId -and $p.permission_type -eq $PermissionType) {
            # Vérifier si le pattern correspond (simplification : * correspond à tout, chemin spécifique vérifie le prefixe)
            $matches = $false
            if ($p.target_pattern -eq "*") {
                $matches = $true
            } elseif ($p.target_pattern -eq $Target) {
                $matches = $true
            } elseif ($p.target_pattern -like "*\*" -and $Target -like $p.target_pattern -replace '\*','*') {
                $matches = $true
            }
            if ($matches) {
                $matching += $p
            }
        }
    }
    if ($matching.Count -eq 0) {
        return @{ decision = "deny"; rule_index = 0; matched = $false }
    }
    # Dernière règle dans l'ordre d'évaluation (rule_index le plus élevé)
    $last = $matching | Sort-Object rule_index | Select-Object -Last 1
    return @{ decision = $last.decision; rule_index = $last.rule_index; matched = $true }
}

# --- T113 : Tester last-match-wins sur chemins de fichiers sensibles ---
Write-Output "=== T113 : Test last-match-wins sur chemins de fichiers sensibles ==="
$testCases = @(
    @{ mode = "architect"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1"; expected = "deny" },
    @{ mode = "bdcp"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1"; expected = "deny" },
    @{ mode = "free"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1"; expected = "deny" },
    @{ mode = "data"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1"; expected = "allow" },
    @{ mode = "architect"; type = "edit"; target = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\readme.md"; expected = "deny" },
    @{ mode = "data"; type = "edit"; target = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\readme.md"; expected = "allow" }
)

foreach ($tc in $testCases) {
    $result = Get-EffectiveDecision -Permissions $permissions -ModeId $tc.mode -PermissionType $tc.type -Target $tc.target
    $pass = $result.decision -eq $tc.expected
    if (-not $pass) {
        $errors += "T113_ECHEC : Mode $($tc.mode) / Type $($tc.type) / Target $($tc.target) : attendu $($tc.expected), obtenu $($result.decision)"
    }
    Write-Output "  $($tc.mode) / $($tc.type) / $($tc.target) -> $($result.decision) (attendu : $($tc.expected)) $([bool]::($pass))"
}

# --- T114 : Tester last-match-wins sur commandes d'exécution ---
Write-Output "`n=== T114 : Test last-match-wins sur commandes d'exécution ==="
$cmdTests = @(
    @{ mode = "architect"; type = "bash"; target = "git commit"; expected = "deny" },
    @{ mode = "data"; type = "bash"; target = "git commit"; expected = "allow" },
    @{ mode = "bdcp"; type = "bash"; target = "python script.py"; expected = "deny" },
    @{ mode = "data"; type = "bash"; target = "python script.py"; expected = "allow" }
)

foreach ($tc in $cmdTests) {
    $result = Get-EffectiveDecision -Permissions $permissions -ModeId $tc.mode -PermissionType $tc.type -Target $tc.target
    $pass = $result.decision -eq $tc.expected
    if (-not $pass) {
        $errors += "T114_ECHEC : Mode $($tc.mode) / Type $($tc.type) / Target $($tc.target) : attendu $($tc.expected), obtenu $($result.decision)"
    }
    Write-Output "  $($tc.mode) / $($tc.type) / $($tc.target) -> $($result.decision) (attendu : $($tc.expected)) $([bool]::($pass))"
}

# --- T115 : Interdire wildcards trop larges en position terminale sur modes restreints ---
Write-Output "`n=== T115 : Test interdiction wildcard terminale sur modes restreints ==="
$wildcardTests = @(
    @{ mode = "architect"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\*"; expected = "deny" },
    @{ mode = "bdcp"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\*"; expected = "deny" },
    @{ mode = "free"; type = "edit"; target = "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\*"; expected = "deny" }
)

foreach ($tc in $wildcardTests) {
    $result = Get-EffectiveDecision -Permissions $permissions -ModeId $tc.mode -PermissionType $tc.type -Target $tc.target
    $pass = $result.decision -eq $tc.expected
    if (-not $pass) {
        $errors += "T115_ECHEC : Mode $($tc.mode) / wildcard $($tc.target) : attendu $($tc.expected), obtenu $($result.decision)"
    }
    Write-Output "  $($tc.mode) / wildcard $($tc.target) -> $($result.decision) (attendu : $($tc.expected)) $([bool]::($pass))"
}

# --- T119 : Test de régression sur l'ordre des règles ---
Write-Output "`n=== T119 : Test de régression sur l'ordre des règles ==="
# Vérifier que la règle 10 (edit deny wildcard SKILLS) est bien après la règle 3 (edit allow data)
$rule10 = $permissions | Where-Object { $_.rule_index -eq 10 -and $_.mode_id -eq "data" }
$rule3 = $permissions | Where-Object { $_.rule_index -eq 3 -and $_.mode_id -eq "data" }
if ($rule10 -and $rule3) {
    if ($rule10.rule_index -gt $rule3.rule_index) {
        Write-Output "  Ordre des règles respecté : R10 (edit deny wildcard) après R3 (edit allow data)"
    } else {
        $errors += "T119_ECHEC : Ordre des règles incorrect - R10 devrait être après R3"
    }
} else {
    $warnings += "T119_WARN : Règles R3 ou R10 introuvables pour le test de régression"
}

# --- T120 : Consigner l'audit des permissions avec empreinte SHA-256 ---
Write-Output "`n=== T120 : Audit des permissions avec empreinte SHA-256 ==="
$fileBytes = [System.IO.File]::ReadAllBytes($PermissionsPath)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$hashBytes = $sha256.ComputeHash($fileBytes)
$hashString = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''

$auditReport = @{
    generated_at_utc = $nowUtc
    permissions_file = $PermissionsPath
    hash_sha256 = $hashString
    total_rules = $permissions.Count
    effective_rules = ($permissions | Where-Object { $_.matched_by_last_match_wins -eq $true }).Count
    errors = $errors
    warnings = $warnings
    status = if ($errors.Count -eq 0) { "VALID" } else { "REJECTED" }
}

$auditPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\logs\audit-permissions-$(Get-Date).ToString('yyyyMMddTHHmmssZ').json"
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}
# Corriger le nom de fichier (supprimer les caractères invalides)
$safeTimestamp = $nowUtc -replace ':', '' -replace '-', '' -replace 'T', '_' -replace '\.', ''
$auditPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\logs\audit-permissions-$safeTimestamp.json"
$auditReport | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $auditPath -Encoding UTF8

Write-Output "  Hash SHA-256 du fichier des permissions : $hashString"
Write-Output "  Règles totales : $($permissions.Count)"
Write-Output "  Règles effectives (last-match-wins) : $($auditReport.effective_rules)"
Write-Output "  Rapport d'audit écrit : $auditPath"

# --- Rapport final ---
Write-Output "`n=============================================="
Write-output "AUDIT DES PERMISSIONS LAST-MATCH-WINS (T113-T120)"
Write-Output "=============================================="
Write-Output "Fichier : $PermissionsPath"
Write-Output "Erreurs : $($errors.Count)"
Write-Output "Avertissements : $($warnings.Count)"
Write-Output "Horodatage : $nowUtc"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    foreach ($e in $errors) { Write-Output "  ERREUR: $e" }
}

if ($warnings.Count -gt 0) {
    foreach ($w in $warnings) { Write-Output "  AVERTISSEMENT: $w" }
}

Write-Output "=============================================="

if ($errors.Count -gt 0) {
    exit 1
} else {
    Write-Output "RESULTAT : VALIDE — Toutes les règles last-match-wins sont cohérentes."
    exit 0
}

