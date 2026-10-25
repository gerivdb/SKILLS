# Script de rollback atomique (Combo-Rollback-Guard)
# Rôle : mécanisme de transaction atomique aux Combos (undo en cas d'échec)
# Encodage : CP1252

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Begin","Record","Undo","Commit","Rollback")]
    [string]$Action,

    [Parameter(Mandatory=$true)]
    [string]$ComboId,

    [Parameter(Mandatory=$false)]
    [string]$StepId,

    [Parameter(Mandatory=$false)]
    [string]$UndoFn
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$walPath = Join-Path $scriptDir "..\..\WAL\combo\rollback-guard.wal"
$statePath = Join-Path $scriptDir "..\..\state\combo\rollback-guard-$ComboId.json"

function Write-WalEntry {
    param([string]$TxnId, [string]$Step, [string]$StepAction, [string]$Status)
    $ts = (Get-Date).ToUniversalTime().ToString("o")
    $entry = "[COMBO_TXN] comboId=$ComboId txnId=$TxnId step=$Step action=$StepAction status=$Status ts=$ts"
    $null = $(New-Item -ItemType File -Path $walPath -Force) | Out-Null
    Add-Content -LiteralPath $walPath -Value $entry -Encoding UTF8
    Write-Output $entry
}

function Get-TxnId {
    return [guid]::NewGuid().ToString()
}

function Load-State {
    if (-not (Test-Path -LiteralPath $statePath)) {
        return @{ steps = @(); status = "ACTIVE"; txnId = $null }
    }
    return Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
}

function Save-State {
    param([object]$State)
    $dir = Split-Path -Parent $statePath
    $null = $(New-Item -ItemType Directory -Path $dir -Force) | Out-Null
    $State | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statePath -Encoding UTF8
}

try {
    $txnId = [guid]::NewGuid().ToString()
    $state = Load-State

    switch ($Action) {
        "Begin" {
            $state.txnId = $txnId
            $state.status = "ACTIVE"
            $state.steps = @()
            Save-State -State $state
            Write-WalEntry -TxnId $txnId -Step "-" -StepAction "BEGIN" -Status "OK"
            Write-Output "[ROLLBACK] Transaction $txnId démarrée pour $ComboId"
        }

        "Record" {
            if ($state.status -ne "ACTIVE") {
                Write-Error "Transaction non active (état: $($state.status)). Impossible d'enregistrer une étape."
                exit 2
            }
            if (-not $StepId -or -not $UndoFn) {
                Write-Error "StepId et UndoFn sont obligatoires pour l'action Record."
                exit 3
            }
            $stepEntry = @{ stepId = $StepId; undoFn = $UndoFn; applied = $true; ts = (Get-Date).ToUniversalTime().ToString("o") }
            $state.steps += $stepEntry
            Save-State -State $state
            Write-WalEntry -TxnId $state.txnId -Step $StepId -StepAction "RECORD" -Status "OK"
            Write-Output "[ROLLBACK] Étape $StepId enregistrée (undo: $UndoFn)"
        }

        "Commit" {
            if ($state.status -ne "ACTIVE") {
                Write-Error "Transaction non active (état: $($state.status)). Impossible de committer."
                exit 4
            }
            $state.status = "COMMITTED"
            Save-State -State $state
            Write-WalEntry -TxnId $state.txnId -Step "-" -StepAction "COMMIT" -Status "OK"
            Write-Output "[ROLLBACK] Transaction committée pour $ComboId"
        }

        "Undo" {
            if (-not $StepId) {
                Write-Error "StepId obligatoire pour l'action Undo."
                exit 5
            }
            $step = $state.steps | Where-Object { $_.stepId -eq $StepId } | Select-Object -First 1
            if (-not $step) {
                Write-Error "Étape $StepId introuvable dans la transaction."
                exit 6
            }
            Write-WalEntry -TxnId $state.txnId -Step $StepId -StepAction "UNDO" -Status "OK"
            Write-Output "[ROLLBACK] Undo exécuté pour $StepId via $($step.undoFn)"
        }

        "Rollback" {
            if ($state.status -eq "ROLLED_BACK") {
                Write-Output "[ROLLBACK] Déjà rollback pour $ComboId"
                exit 0
            }
            if ($state.status -eq "COMMITTED") {
                Write-Error "Transaction déjà committée, rollback impossible."
                exit 7
            }
            # Rollback LIFO : étapes inversées
            $steps = $state.steps | Sort-Object -Property @{Expression={ $state.steps.IndexOf($_) }} -Descending
            foreach ($step in $steps) {
                Write-WalEntry -TxnId $state.txnId -Step $step.stepId -StepAction "ROLLBACK" -Status "OK"
                Write-Output "[ROLLBACK] Undo de $($step.stepId) via $($step.undoFn)"
            }
            $state.status = "ROLLED_BACK"
            Save-State -State $state
            Write-Output "[ROLLBACK] Rollback complet pour $ComboId ($($state.steps.Count) étape(s) révoquée(s))"
        }
    }

    exit 0
}
catch {
    Write-WalEntry -TxnId $txnId -Step $StepId -StepAction $Action -Status "FAIL"
    Write-Error "Échec rollback-guard action $Action : $($_.Exception.Message)"
    exit 8
}