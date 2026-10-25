# Script d'exécution de pipeline de skills (Combo-Pipeline-Executor)
# Rôle : enchaîne une série de skills unitaires avec passage déterministe de contexte via JSON-RPC/stdin
# Encodage : CP1252

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$ComboFile,

    [Parameter(Mandatory=$false)]
    [string[]]$Skills,

    [Parameter(Mandatory=$false)]
    [hashtable]$Context = @{}
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$walPath = Join-Path $scriptDir "..\..\WAL\combo\pipeline-executor.wal"

function Write-WalEntry {
    param([string]$ComboId, [string]$SkillId, [string]$Status, [string]$ContextHash)
    $ts = (Get-Date).ToUniversalTime().ToString("o")
    $entry = "[COMBO_EXEC] comboId=$ComboId skill=$SkillId status=$Status contextHash=$ContextHash ts=$ts"
    $null = $(New-Item -ItemType File -Path $walPath -Force) | Out-Null
    Add-Content -LiteralPath $walPath -Value $entry -Encoding UTF8
    Write-Output $entry
}

function Get-ContextHash {
    param([hashtable]$Ctx)
    $json = $Ctx | ConvertTo-Json -Depth 5
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hash = $sha.ComputeHash($bytes)
    return [BitConverter]::ToString($hash).Replace("-","").ToLower()
}

function Invoke-SkillStep {
    param([string]$SkillId, [hashtable]$InputContext)
    # Simulation d'exécution d'un skill unitaire via JSON-RPC sur stdin
    $rpcRequest = @{
        jsonrpc = "2.0"
        method  = "skill.execute"
        params  = @{ skillId = $SkillId; context = $InputContext }
        id      = [guid]::NewGuid().ToString()
    } | ConvertTo-Json -Depth 5

    $stdinInput = $rpcRequest
    Write-Output "[JSON-RPC] ? $SkillId : $($rpcRequest | ConvertTo-Json -Compress)"
    $outputContext = @{ skillId = $SkillId; executed = $true; output = "ok"; timestamp = (Get-Date).ToUniversalTime().ToString("o") }
    return $outputContext
}

try {
    $comboId = "unknown"
    $pipelineContext = $Context

    if ($ComboFile -and (Test-Path -LiteralPath $ComboFile)) {
        $comboDef = Get-Content -LiteralPath $ComboFile -Raw | ConvertFrom-Json
        $comboId = $comboDef.comboId
        if ($comboDef.skills) {
            $Skills = $comboDef.skills.id
        }
        if ($comboDef.context) {
            $pipelineContext = $comboDef.context
        }
    }

    if (-not $Skills -or $Skills.Count -eq 0) {
        Write-Error "Aucun skill défini pour le pipeline."
        exit 1
    }

    Write-Output "[COMBO] Démarrage pipeline $comboId avec $($Skills.Count) skill(s)"

    $i = 0
    foreach ($skillId in $Skills) {
        $i++
        $stepInput = @{
            skillId = $skillId
            step = $i
            total = $Skills.Count
            context = $pipelineContext
        }

        $result = Invoke-SkillStep -SkillId $skillId -InputContext $stepInput
        $ctxHash = Get-ContextHash -Ctx $pipelineContext

        Write-WalEntry -ComboId $comboId -SkillId $skillId -Status "OK" -ContextHash $ctxHash

        # Passage déterministe du contexte au skill suivant
        $pipelineContext = @{
            previousSkill = $skillId
            previousResult = $result
            inheritedContext = $pipelineContext
        }
    }

    Write-Output "[COMBO] Pipeline $comboId terminé avec succès ($i étapes)"
    exit 0
}
catch {
    $ctxHash = Get-ContextHash -Ctx $pipelineContext
    Write-WalEntry -ComboId $comboId -SkillId $Skills[$i-1] -Status "FAIL" -ContextHash $ctxHash
    Write-Error "Échec du pipeline à l'étape $i : $($_.Exception.Message)"
    exit 2
}