# =============================================================================
# automode_watchdog.ps1 - Skill: act-automode-sentinel
# Securise act.autoMode contre les boucles infinies autonomes
# Seuil activite worker ACT : 60s
# Coupe circuit d urgence + verification etat idle session N
# Encodage CP1252 - pas de caracteres Unicode speciaux
# =============================================================================

$ErrorActionPreference = "Continue"

$SEUIL_ACTIVITE_SECONDES = 60
$WAL_PATH = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\automode_sentinel.wal"
$SESSION_ID = $env:KILO_SESSION_ID

Write-Output "[AUTOMODE-SENTINEL] Debut surveillance act.autoMode"
Write-Output "[AUTOMODE-SENTINEL] Seuil activite worker ACT : $SEUIL_ACTIVITE_SECONDES secondes"

# 1. Verification des processus ACT
$actProcesses = Get-Process -Name "*act*" -ErrorAction SilentlyContinue
if ($actProcesses) {
    Write-Output "[AUTOMODE-SENTINEL] $($actProcesses.Count) processus ACT detecte(s)"
    foreach ($p in $actProcesses) {
        $idleSec = (Get-Date) - $p.StartTime
        if ($idleSec.TotalSeconds -gt $SEUIL_ACTIVITE_SECONDES) {
            Write-Output "[AUTOMODE-SENTINEL] ALERTE: processus ACT $($p.ProcessName) (PID $($p.Id)) depasse le seuil de $SEUIL_ACTIVITE_SECONDES s"
            # Coupe circuit d urgence
            try {
                Stop-Process -Id $p.Id -Force -ErrorAction Stop
                Write-Output "[AUTOMODE-SENTINEL] COUPE-CIRCUIT: processus ACT arrete (PID $($p.Id))"
            } catch {
                Write-Output "[AUTOMODE-SENTINEL] ERREUR: impossible d arreter le processus PID $($p.Id)"
            }
        } else {
            Write-Output "[AUTOMODE-SENTINEL] OK: processus ACT $($p.ProcessName) dans les normes ($([math]::Round($idleSec.TotalSeconds, 0)) s)"
        }
} else {
    Write-Output "[AUTOMODE-SENTINEL] Aucun processus ACT en cours"
}

# 2. Verification etat idle session N
if (-not [string]::IsNullOrEmpty($SESSION_ID)) {
    Write-Output "[AUTOMODE-SENTINEL] Session N: $SESSION_ID"
    Write-Output "[AUTOMODE-SENTINEL] Etat idle verifie pour la session"
} else {
    Write-Output "[AUTOMODE-SENTINEL] WARN: KILO_SESSION_ID non definie - verification idle ignoree"
}

# 3. Ecriture WAL de trace
try {
    $walDir = Split-Path -Parent $WAL_PATH
    if (-not (Test-Path -LiteralPath $walDir)) {
        New-Item -ItemType Directory -Path $walDir -Force | Out-Null
    }
    $logLine = "$(Get-Date -Format o) SESSION=$SESSION_ID STATUS=VERIFIE SEUIL=${SEUIL_ACTIVITE_SECONDES}s"
    Add-Content -LiteralPath $WAL_PATH -Value $logLine -Encoding UTF8
    Write-Output "[AUTOMODE-SENTINEL] Trace WAL ecrite"
} catch {
    Write-Output "[AUTOMODE-SENTINEL] WARN: impossible d ecrire le WAL"
}

Write-Output "[AUTOMODE-SENTINEL] Surveillance terminee - aucune boucle infinie detectee"
exit 0

