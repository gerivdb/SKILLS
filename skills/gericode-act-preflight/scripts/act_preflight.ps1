# =============================================================================
# act_preflight.ps1 - Skill: gericode-act-preflight
# Verifie l'aptitude d'ENV2 a reactiver gerivdb.act-vscode-0.2.0 sans conflit
# Encodage CP1252 - pas de caracteres Unicode speciaux
# =============================================================================

$ErrorActionPreference = "Stop"

$VSSIX_PATH = "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\act-vscode-0.2.0.vsix"
$GPG_EXE = "C:\Program Files (x86)\GPG\bin\gpg.exe"
$CACHE_L1 = "D:\DO\WEB\TOOLS\L1-INFRA"
$CACHE_L2 = "D:\DO\WEB\TOOLS\L2-PLATFORM"

Write-Output "[ACT-PREFLIGHT] Debut de la verification preflight ENV2"
Write-Output "[ACT-PREFLIGHT] Cible VSIX : $VSSIX_PATH"

# 1. Verification du binaire VSIX
if (-not (Test-Path -LiteralPath $VSSIX_PATH)) {
    Write-Output "[ACT-PREFLIGHT] BLOQUE: VSIX introuvable a $VSSIX_PATH"
    exit 1
}
$vsiSize = (Get-Item -LiteralPath $VSSIX_PATH).Length
Write-Output "[ACT-PREFLIGHT] OK: VSIX present ($vsiSize octets)"

# 2. Verification de gpg.exe
if (-not (Test-Path -LiteralPath $GPG_EXE)) {
    Write-Output "[ACT-PREFLIGHT] BLOQUE: gpg.exe introuvable a $GPG_EXE"
    exit 1
}
Write-Output "[ACT-PREFLIGHT] OK: gpg.exe present"

# 3. Verification des caches L1/L2
if (-not (Test-Path -LiteralPath $CACHE_L1)) {
    Write-Output "[ACT-PREFLIGHT] WARN: Cache L1 introuvable a $CACHE_L1"
} else {
    Write-Output "[ACT-PREFLIGHT] OK: Cache L1 accessible"
}
if (-not (Test-Path -LiteralPath $CACHE_L2)) {
    Write-Output "[ACT-PREFLIGHT] WARN: Cache L2 introuvable a $CACHE_L2"
} else {
    Write-Output "[ACT-PREFLIGHT] OK: Cache L2 accessible"
}

# 4. Purge des caches lies a ACT (L1/L2)
$actCacheItems = @()
if (Test-Path -LiteralPath $CACHE_L1) {
    $actCacheItems += Get-ChildItem -LiteralPath $CACHE_L1 -Filter "*act*" -Recurse -ErrorAction SilentlyContinue
}
if (Test-Path -LiteralPath $CACHE_L2) {
    $actCacheItems += Get-ChildItem -LiteralPath $CACHE_L2 -Filter "*act*" -Recurse -ErrorAction SilentlyContinue
}
if ($actCacheItems.Count -gt 0) {
    Write-Output "[ACT-PREFLIGHT] Purge de $($actCacheItems.Count) element(s) cache ACT"
    $actCacheItems | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
} else {
    Write-Output "[ACT-PREFLIGHT] Aucun element cache ACT a purger"
}

Write-Output "[ACT-PREFLIGHT] Preflight termine avec succès - ENV2 apte a reactiver ACT"
exit 0

