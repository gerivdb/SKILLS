#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validateur de configuration des modes KiloCode sur ENV2 (Phase 11, T108).

.DESCRIPTION
    Vérifie la cohérence de la matrice des modes (modes-matrix.json) :
    - Existence des fichiers de configuration référencés
    - Présence des champs requis (mode_id, kind, vocation, write_policy, lease_required, risk_level, entry_conditions, exit_conditions)
    - Absence de doublon de mode_id
    - Cohérence des champs spécifiques (bdcp_clapet_default sur bdcp uniquement, lease_required true sur data uniquement)

.PARAMETER MatrixPath
    Chemin vers le fichier modes-matrix.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json).

.PARAMETER SchemaPath
    Chemin vers le fichier modes-matrix.schema.json (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.schema.json).

.EXAMPLE
    ./validate-modes.ps1

.EXAMPLE
    ./validate-modes.ps1 -MatrixPath "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json"

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md, SPEC-SKILL-FORMAT.md, kilo-modes-bdcp-free.md
    Phase 11, T108 — Créer validateur de configuration des modes
#>

[CmdletBinding()]
param(
    [string]$MatrixPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.json",
    [string]$SchemaPath = "D:\DO\WEB\TOOLS\L4-TOOLS\L4-TOOLS\SKILLS\distill\modes-matrix.schema.json"
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $MatrixPath)) {
    Write-Error "Fichier de matrice introuvable : $MatrixPath"
    exit 1
}
if (-not (Test-Path -LiteralPath $SchemaPath)) {
    Write-Error "Fichier de schéma introuvable : $SchemaPath"
    exit 1
}

# --- Lecture de la matrice ---
$matrixContent = Get-Content -LiteralPath $MatrixPath -Raw -ErrorAction Stop
$matrix = $matrixContent | ConvertFrom-Json -ErrorAction Stop

# --- 1. Vérifier absence de doublon de mode_id ---
$modeIds = @()
foreach ($m in $matrix.modes) {
    if ($modeIds -contains $m.mode_id) {
        $errors += "DOUBLETON_MODE_ID : Le mode_id '$($m.mode_id)' apparaît plusieurs fois dans la matrice."
    }
    $modeIds += $m.mode_id
}

# --- 2. Vérifier chaque mode : champs requis + fichiers de config ---
$requiredFields = @("mode_id", "kind", "vocation", "write_policy", "lease_required", "risk_level", "entry_conditions", "exit_conditions", "config_path", "source_shard")
$validKinds = @("agent_definition", "rule_profile")
$validVocations = @("audit", "lecture", "execution", "ecriture", "diagnostic", "pontage", "orchestration")
$validWritePolicies = @("read_only", "lease_required")
$validRiskLevels = @("low", "medium", "high")

foreach ($m in $matrix.modes) {
    $modeId = $m.mode_id

    # Champs requis
    foreach ($field in $requiredFields) {
        if (-not $m.PSObject.Properties.Name -contains $field) {
            $errors += "CHAMP_MANQUANT : Le mode '$modeId' ne contient pas le champ obligatoire '$field'."
        }
    }

    # Valeurs valides
    if ($m.kind -and $validKinds -notcontains $m.kind) {
        $errors += "KIND_INVALIDE : Le mode '$modeId' a un kind '$($m.kind)' non reconnu (valeurs autorisées : $($validKinds -join ', '))."
    }
    if ($m.vocation -and $validVocations -notcontains $m.vocation) {
        $errors += "VOCATION_INVALIDE : Le mode '$modeId' a une vocation '$($m.vocation)' non reconnue."
    }
    if ($m.write_policy -and $validWritePolicies -notcontains $m.write_policy) {
        $errors += "WRITE_POLICY_INVALIDE : Le mode '$modeId' a un write_policy '$($m.write_policy)' non reconnu."
    }
    if ($m.risk_level -and $validRiskLevels -notcontains $m.risk_level) {
        $errors += "RISQUE_INVALIDE : Le mode '$modeId' a un risque '$($m.risk_level)' non reconnu."
    }

    # Fichier de config existe
    if ($m.config_path) {
        if (-not (Test-Path -LiteralPath $m.config_path)) {
            $errors += "CONFIG_INTROUVABLE : Le mode '$modeId' référence un fichier de config introuvable : $($m.config_path)"
        }
    }

    # Cohérence bdcp_clapet_default : présent sur bdcp, null sur les autres
    if ($m.mode_id -eq "bdcp") {
        if ($m.bdcp_clapet_default -ne "closed") {
            $errors += "CLAPET_BDCP : Le mode 'bdcp' doit avoir bdcp_clapet_default = 'closed', valeur trouvée : '$($m.bdcp_clapet_default)'."
        }
    } else {
        if ($m.bdcp_clapet_default -and $m.bdcp_clapet_default -ne $null) {
            $warnings += "CLAPET_BDCP_INUTILE : Le mode '$modeId' a un champ bdcp_clapet_default alors qu'il n'est pas le mode bdcp."
        }
    }

    # Cohérence lease_required : true sur data, false sur les autres
    if ($m.mode_id -eq "data") {
        if ($m.lease_required -ne $true) {
            $errors += "LEASE_REQUIRED : Le mode 'data' doit avoir lease_required = true."
        }
    } else {
        if ($m.lease_required -eq $true) {
            $warnings += "LEASE_REQUIRED_INUTILE : Le mode '$modeId' a lease_required = true alors qu'il n'est pas le mode data."
        }
    }

    # write_policy cohérent avec kind
    if ($m.kind -eq "rule_profile" -and $m.write_policy -ne "read_only") {
        $warnings += "WRITE_POLICY_INCOHERENT : Le mode '$modeId' (rule_profile) devrait avoir write_policy = read_only."
    }
}

# --- 3. Vérifier qu'il y a au moins un mode de chaque type ---
$hasAgentDef = ($matrix.modes | Where-Object { $_.kind -eq "agent_definition" }).Count -gt 0
$hasRuleProfile = ($matrix.modes | Where-Object { $_.kind -eq "rule_profile" }).Count -gt 0
if (-not $hasAgentDef) {
    $warnings += "AUCUN_AGENT_DEFINITION : Aucun mode de type agent_definition dans la matrice."
}
if (-not $hasRuleProfile) {
    $warnings += "AUCUN_RULE_PROFILE : Aucun mode de type rule_profile dans la matrice."
}

# --- Rapport ---
Write-Output "=============================================="
Write-Output "VALIDATION DES MODES KILOCODE (T108)"
Write-Output "=============================================="
Write-Output "Matrice    : $MatrixPath"
Write-Output "Schéma     : $SchemaPath"
Write-Output "Modes      : $($matrix.modes.Count)"
Write-Output "Erreurs    : $($errors.Count)"
Write-Output "Avertissements: $($warnings.Count)"
Write-Output "Horodatage : $nowUtc"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    Write-Output "ERREURS BLOQUANTES :"
    foreach ($e in $errors) { Write-Output "  - $e" }
}

if ($warnings.Count -gt 0) {
    Write-Output "AVERTISSEMENTS :"
    foreach ($w in $warnings) { Write-Output "  - $w" }
}

Write-Output "=============================================="

if ($errors.Count -gt 0) {
    Write-Output "RESULTAT : REJETE — Corrigez les erreurs ci-dessus."
    exit 1
} else {
    Write-Output "RESULTAT : VALIDE — La matrice des modes est cohérente."
    exit 0
}
