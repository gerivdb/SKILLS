#!/usr/bin/env pwsh
# ============================================================================
# deploy.ps1 — Déploiement GAS via API REST
# Empreinte WAL : 0x243
#
# Déploie des fichiers .gs et le manifeste appscript.json vers un projet
# Google Apps Script distant via l'API REST (PUT /content), puis crée une
# version et un déploiement Web App.
# ============================================================================
param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptId,
    [Parameter(Mandatory=$true)]
    [string]$AccessToken,
    [Parameter(Mandatory=$true)]
    [string[]]$Files,
    [Parameter(Mandatory=$false)]
    [string]$Description = "Deploy via gas-rest-deployer skill"
)

$ErrorActionPreference = "Stop"
$uri = "https://script.googleapis.com/v1/projects/${ScriptId}/content"

# --- Construire le payload des fichiers ---
$fileObjects = @()
foreach ($f in $Files) {
    if (-not (Test-Path $f)) {
        Write-Error "Fichier introuvable : $f"
        exit 1
    }
    $ext = [System.IO.Path]::GetExtension($f).ToLower()
    $type = if ($ext -eq ".json") { "JSON" } else { "SERVER_JS" }
    $content = Get-Content -Path $f -Raw
    $name = [System.IO.Path]::GetFileNameWithoutExtension($f)
    $fileObjects += @{
        name  = $name
        type  = $type
        source = $content
    }
    Write-Host "[OK] Lu : $f ($type) - $($content.Length) chars"
}

$body = @{ files = $fileObjects } | ConvertTo-Json -Depth 10
$headers = @{
    Authorization  = "Bearer $AccessToken"
    "Content-Type" = "application/json"
}

# --- PUT /content ---
Write-Host "=== PUT /content ==="
Write-Host "URI : $uri"
try {
    $response = Invoke-RestMethod -Uri $uri -Method Put -Headers $headers -Body $body -ContentType "application/json" -ErrorAction Stop
    Write-Host "[OK] Projet GAS mis à jour. Fichiers : $($response.files.Count)"
} catch {
    Write-Error "Échec PUT /content : $($_.Exception.Message)"
    exit 1
}

# --- Créer une version ---
$versionUri = "https://script.googleapis.com/v1/projects/${ScriptId}/versions"
$versionBody = @{ description = $Description } | ConvertTo-Json
try {
    $versionRes = Invoke-RestMethod -Uri $versionUri -Method Post -Headers $headers -Body $versionBody -ContentType "application/json" -ErrorAction Stop
    $versionNumber = $versionRes.versionNumber
    Write-Host "[OK] Version créée : $versionNumber"
} catch {
    Write-Error "Échec création version : $($_.Exception.Message)"
    exit 1
}

# --- Créer un déploiement ---
$deployUri = "https://script.googleapis.com/v1/projects/${ScriptId}/deployments"
$deployBody = @{
    versionNumber     = [int]$versionNumber
    manifestFileName  = "appsscript"
    description       = $Description
} | ConvertTo-Json -Depth 3
try {
    $deployRes = Invoke-RestMethod -Uri $deployUri -Method Post -Headers $headers -Body $deployBody -ContentType "application/json" -ErrorAction Stop
    $deploymentId = $deployRes.deploymentId
    $webAppUrl = $deployRes.entryPoints[0].webApp.url
    Write-Host "[OK] Déploiement créé : $deploymentId"
    Write-Host "[URL] $webAppUrl"
} catch {
    Write-Error "Échec création déploiement : $($_.Exception.Message)"
    exit 1
}

Write-Host "=== DÉPLOIEMENT TERMINÉ ==="
Write-Host "Version : $versionNumber"
Write-Host "Deployment ID : $deploymentId"
Write-Host "URL Web App : $webAppUrl"
