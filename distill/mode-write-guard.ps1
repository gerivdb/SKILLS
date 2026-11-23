#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Garde-fou d'exécution mode-write-guard.ps1 (Phase 13, T123).

.DESCRIPTION
    Vérifie avant toute opération d'écriture sur ENV2 que :
    1. Le mode actif autorise l'écriture (write_policy = lease_required, pas read_only)
    2. Un bail actif couvre le territoire cible (via claim-lease.ps1 / leases.json)
    3. Le mode n'est pas en lecture seule (architect, bdcp, free)

    Rejette immédiatement toute écriture en mode read_only ou sans bail actif.
    Journalise chaque blocage d'écriture (mode, cible, raison, horodatage UTC).

.PARAMETER ModeId
    Identifiant du mode actif (ex: architect, data, bdcp, free).

.PARAMETER TargetPath
    Chemin cible de l'opération d'écriture.

.PARAMETER Operation
    Type d'opération (ex: write, edit, git_push, set_content, out_file, rm, mv).

.PARAMETER LeasePath
    Chemin vers le fichier leases.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json).

.PARAMETER PermissionsPath
    Chemin vers le fichier effective-permissions.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\effective-permissions.json).

.PARAMETER LogPath
    Chemin vers le journal des blocages (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\write-guard.log).

.EXAMPLE
    ./mode-write-guard.ps1 -ModeId data -TargetPath "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1" -Operation write

.EXAMPLE
    ./mode-write-guard.ps1 -ModeId architect -TargetPath "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\test.ps1" -Operation write

.NOTES
    Phase 13, T123 — Créer mode-write-guard.ps1
    Dépend : effective-permissions.json, leases.json, claim-lease.ps1
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ModeId,

    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [Parameter(Mandatory = $true)]
    [string]$Operation,

    [string]$LeasePath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\leases.json",

    [string]$PermissionsPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\effective-permissions.json",

    [string]$LogPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs\write-guard.log"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $PermissionsPath)) {
    Write-Error "Fichier effective-permissions.json introuvable : $PermissionsPath"
    exit 1
}
if (-not (Test-Path -LiteralPath $LeasePath)) {
    Write-Error "Fichier leases.json introuvable : $LeasePath"
    exit 1
}

# --- Lecture de la matrice des permissions ---
$permissions = (Get-Content -LiteralPath $PermissionsPath -Raw | ConvertFrom-Json).permissions
$leases = (Get-Content -LiteralPath $LeasePath -Raw | ConvertFrom-Json).leases

# --- Fonction : obtenir la décision effective pour un (mode, type, target) ---
function Get-EffectiveDecision {
    param([array]$Permissions, [string]$ModeId, [string]$PermissionType, [string]$Target)
    $matching = @()
    foreach ($p in $Permissions) {
        if ($p.mode_id -eq $ModeId -and $p.permission_type -eq $PermissionType) {
            $matches = $false
            if ($p.target_pattern -eq "*") {
                $matches = $true
            } elseif ($p.target_pattern -eq $Target) {
                $matches = $true
            } elseif ($Target -like $p.target_pattern) {
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
    $last = $matching | Sort-Object rule_index | Select-Object -Last 1
    return @{ decision = $last.decision; rule_index = $last.rule_index; matched = $true }
}

# --- Fonction : vérifier si un bail actif couvre le territoire ---
function Get-ActiveLeaseForTarget {
    param([array]$Leases, [string]$Target)
    $now = (Get-Date).ToUniversalTime()
    foreach ($l in $Leases) {
        if ($l.status -ne "active") { continue }
        $expires = [datetime]$l.expires_utc
        $expires = $expires.ToUniversalTime()
        if ($expires -lt $now) { continue }
        # Vérifier si le Target est couvert par un scope_paths du bail
        foreach ($scope in $l.scope_paths) {
            if ($Target -like $scope) {
                return $l
            }
        }
    }
    return $null
}

# --- Déterminer le type de permission selon l'opération ---
$permissionType = "edit"
switch ($Operation) {
    { $_ -in @("git_push", "set_content", "out_file", "rm", "mv", "remove-item", "copy-item") } { $permissionType = "edit" }
    { $_ -in @("bash", "python", "pwsh", "zsh") } { $permissionType = "bash" }
    { $_ -eq "mcp" } { $permissionType = "mcp" }
    default { $permissionType = "edit" }
}

# --- Obtenir la décision effective ---
$decision = Get-EffectiveDecision -Permissions $permissions -ModeId $ModeId -PermissionType $permissionType -Target $TargetPath

# --- Vérifier le bail si le mode nécessite un bail actif ---
$leaseActive = $false
$leaseInfo = $null
if ($decision.decision -eq "allow") {
    $lease = Get-ActiveLeaseForTarget -Leases $leases -Target $TargetPath
    if ($lease) {
        $leaseActive = $true
        $leaseInfo = $lease
    }
}

# --- Décision finale : autoriser ou rejeter ---
$allowed = $false
$rejectReason = ""

if ($decision.decision -eq "deny") {
    $allowed = $false
    $rejectReason = "Mode $ModeId n'autorise pas l'opération $Operation (décision last-match-wins : deny)"
} elseif ($decision.decision -eq "allow" -and -not $leaseActive) {
    # Si le mode nécessite un bail et qu'aucun bail n'est actif, rejeter
    $allowed = $false
    $rejectReason = "Aucun bail actif couvrant la cible $TargetPath (mode $ModeId nécessite lease_required)"
} elseif ($decision.decision -eq "allow" -and $leaseActive) {
    $allowed = $true
    $rejectReason = $null
}

# --- Journaliser le blocage ---
if (-not (Test-Path -LiteralPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs")) {
    New-Item -ItemType Directory -Force -Path "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\logs" | Out-Null
}

$logEntry = "[$nowUtc] Mode=$ModeId Operation=$Operation Target=$TargetPath Decision=$([bool]::($allowed)) Reason=$rejectReason"
Add-Content -LiteralPath $LogPath -Value $logEntry -Encoding UTF8

# --- Rapport ---
Write-Output "=============================================="
Write-output "MODE-WRITE-GUARD (T123)"
Write-Output "=============================================="
Write-Output "Mode        : $ModeId"
Write-Output "Opération   : $Operation"
Write-Output "Cible       : $TargetPath"
Write-Output "Décision    : $([bool]::($allowed))"
Write-Output "Raison      : $rejectReason"
Write-Output "Bail actif  : $leaseActive"
Write-Output "Journal     : $LogPath"
Write-Output "=============================================="

if (-not $allowed) {
    Write-Output "RESULTAT : ÉCRITURE BLOQUÉE"
    exit 1
} else {
    Write-Output "RESULTAT : ÉCRITURE AUTORISÉE"
    exit 0
}

