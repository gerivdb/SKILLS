# enforce.ps1
# strata-boundary-enforcer - Interdiction de modification L0 par un skill L4 sans mandat Citoyen
# Conforme à la règle strata-boundary-enforcer (intent_hash: 0xSKILL_STRATA_BOUNDARY_ENFORCER_20261025)
# Encodage strict CP1252 - Aucun caractère UTF-8 exotique

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SkillId,

    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [Parameter(Mandatory = $true)]
    [string]$TargetStratum,

    [Parameter(Mandatory = $false)]
    [string]$CitizenMandate,

    [Parameter(Mandatory = $false)]
    [ValidateSet("read", "write", "delete", "modify")]
    [string]$Operation = "read"
)

$ErrorActionPreference = "Stop"

function Write-Log([string]$message) {
    $ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    Write-Output "[$ts] $message"
}

function Test-L0Path([string]$path) {
    return $path -match "^D:\\DO\\WEB\\TOOLS\\L0-CANON\\"
}

# === EXECUTION PRINCIPALE ===
$isL0 = Test-L0Path -path $TargetPath
$mandateRequired = $isL0 -and ($TargetStratum -eq "L0" -or $TargetStratum -eq "L0-CANON")
$authorized = $true
$reason = "Opération autorisée"

if ($mandateRequired) {
    if (-not $CitizenMandate) {
        $authorized = $false
        $reason = "REFUSÉ : Modification L0 par skill L4 sans mandat Citoyen explicite"
    } else {
        $reason = "AUTORISÉ : Mandat Citoyen présent pour accès L0"
    }
}

if ($authorized) {
    Write-Log "ACCÈS AUTORISÉ : Skill $SkillId -> $TargetPath (strate $TargetStratum, opération $Operation)"
} else {
    Write-Log "ACCÈS REFUSÉ : Skill $SkillId -> $TargetPath (strate $TargetStratum, opération $Operation) : $reason"
}

Write-Output "authorized=$authorized"
Write-Output "reason=$reason"
Write-Output "mandate_required=$mandateRequired"

if (-not $authorized) {
    exit 1
}

exit 0
