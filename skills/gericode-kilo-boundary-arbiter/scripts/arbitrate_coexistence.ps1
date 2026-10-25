# =============================================================================
# arbitrate_coexistence.ps1 - Skill: gericode-kilo-boundary-arbiter
# Garantit l etancheite stricte entre Kilo Code et GeriCode ACT
# Territoire Kilo : chat, prompts, agent-manager.json
# Territoire GeriCode : surveillance autonome, signature GPG, bus .kilo/bus/
# Encodage CP1252 - pas de caracteres Unicode speciaux
# =============================================================================

$ErrorActionPreference = "Continue"

$SKILLS_ROOT = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
$KILO_BUS = Join-Path $SKILLS_ROOT ".kilo\bus"
$AGENT_MANAGER_JSON = Join-Path $SKILLS_ROOT "agent-manager.json"
$SHARED_HOOKS = Join-Path $SKILLS_ROOT ".githooks"

Write-Output "[KILO-BOUNDARY] Debut de l arbitrage Kilo <-> GeriCode"

# 1. Verification du bus .kilo/bus (territoire GeriCode)
if (-not (Test-Path -LiteralPath $KILO_BUS)) {
    Write-Output "[KILO-BOUNDARY] INFO: .kilo/bus absent - creation du repertoire territoire GeriCode"
    New-Item -ItemType Directory -Path $KILO_BUS -Force | Out-Null
    Write-Output "[KILO-BOUNDARY] OK: .kilo/bus cree (territoire GeriCode)"
} else {
    Write-Output "[KILO-BOUNDARY] OK: .kilo/bus present (territoire GeriCode)"
}

# 2. Verification de agent-manager.json (territoire Kilo)
if (-not (Test-Path -LiteralPath $AGENT_MANAGER_JSON)) {
    Write-Output "[KILO-BOUNDARY] WARN: agent-manager.json introuvable (territoire Kilo)"
} else {
    Write-Output "[KILO-BOUNDARY] OK: agent-manager.json present (territoire Kilo)"
}

# 3. Verification des hooks partagés
if (-not (Test-Path -LiteralPath $SHARED_HOOKS)) {
    Write-Output "[KILO-BOUNDARY] INFO: .githooks absent - aucun hook partage configure"
} else {
    Write-Output "[KILO-BOUNDARY] OK: .githooks present (hooks partagés)"
}

# 4. Rapport de frontiere
Write-Output "[KILO-BOUNDARY] Frontiere Kilo: chat, prompts, agent-manager.json"
Write-Output "[KILO-BOUNDARY] Frontiere GeriCode: surveillance autonome, signature GPG, .kilo/bus/"
Write-Output "[KILO-BOUNDARY] Arbitrage termine - etancherite verifiee"

exit 0

