# Script de catalogue de recettes (Combo-Recipe-Catalog)
# Rôle : liste et valide les recettes de combo
# Encodage : CP1252

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("List","Validate","Get")]
    [string]$Action,

    [Parameter(Mandatory=$false)]
    [string]$Recipe,

    [Parameter(Mandatory=$false)]
    [string]$CatalogFile
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$walPath = Join-Path $scriptDir "..\..\WAL\combo\recipe-catalog.wal"
$catalogPath = $CatalogFile
if (-not $catalogPath) {
    $catalogPath = Join-Path $scriptDir "..\..\catalogs\combo-recipes.json"
}

function Write-WalEntry {
    param([string]$CatalogAction, [string]$RecipeId, [string]$Status, [int]$SkillsCount)
    $ts = (Get-Date).ToUniversalTime().ToString("o")
    $entry = "[COMBO_CATALOG] action=$CatalogAction recipe=$RecipeId status=$Status skills=$SkillsCount ts=$ts"
    $null = $(New-Item -ItemType File -Path $walPath -Force) | Out-Null
    Add-Content -LiteralPath $walPath -Value $entry -Encoding UTF8
    Write-Output $entry
}

function Load-Catalog {
    if (-not (Test-Path -LiteralPath $catalogPath)) {
        return @{ catalogVersion = "1.0.0"; recipes = @() }
    }
    return Get-Content -LiteralPath $catalogPath -Raw | ConvertFrom-Json
}

function Validate-Recipe {
    param([object]$Recipe)
    $errors = @()
    if (-not $Recipe.id) { $errors += "id manquant" }
    if (-not $Recipe.name) { $errors += "name manquant" }
    if (-not $Recipe.skills -or $Recipe.skills.Count -eq 0) { $errors += "aucune compétence déclarée" }
    return $errors
}

try {
    $catalog = Load-Catalog

    switch ($Action) {
        "List" {
            Write-Output "[CATALOG] Version $($catalog.catalogVersion) — $($catalog.recipes.Count) recette(s)"
            foreach ($r in $catalog.recipes) {
                Write-Output "  - $($r.id) v$($r.version) : $($r.description) ($($r.skills.Count) skill(s))"
            }
            Write-WalEntry -CatalogAction "List" -RecipeId "-" -Status "OK" -SkillsCount 0
        }

        "Validate" {
            if (-not $Recipe) {
                Write-Error "Le paramètre -Recipe est obligatoire pour l'action Validate."
                exit 1
            }
            $target = $catalog.recipes | Where-Object { $_.id -eq $Recipe } | Select-Object -First 1
            if (-not $target) {
                Write-WalEntry -CatalogAction "Validate" -RecipeId $Recipe -Status "FAIL" -SkillsCount 0
                Write-Error "Recette '$Recipe' introuvable dans le catalogue."
                exit 2
            }
            $errors = Validate-Recipe -Recipe $target
            if ($errors.Count -gt 0) {
                Write-WalEntry -CatalogAction "Validate" -RecipeId $Recipe -Status "FAIL" -SkillsCount $target.skills.Count
                Write-Error "Recette '$Recipe' invalide : $($errors -join ', ')"
                exit 3
            }
            Write-WalEntry -CatalogAction "Validate" -RecipeId $Recipe -Status "OK" -SkillsCount $target.skills.Count
            Write-Output "[CATALOG] Recette '$Recipe' valide ($($target.skills.Count) compétence(s))"
        }

        "Get" {
            if (-not $Recipe) {
                Write-Error "Le paramètre -Recipe est obligatoire pour l'action Get."
                exit 4
            }
            $target = $catalog.recipes | Where-Object { $_.id -eq $Recipe } | Select-Object -First 1
            if (-not $target) {
                Write-WalEntry -CatalogAction "Get" -RecipeId $Recipe -Status "FAIL" -SkillsCount 0
                Write-Error "Recette '$Recipe' introuvable dans le catalogue."
                exit 5
            }
            Write-WalEntry -CatalogAction "Get" -RecipeId $Recipe -Status "OK" -SkillsCount $target.skills.Count
            $target | ConvertTo-Json -Depth 5
        }
    }

    exit 0
}
catch {
    Write-WalEntry -CatalogAction $Action -RecipeId $Recipe -Status "FAIL" -SkillsCount 0
    Write-Error "Échec catalogue action $Action : $($_.Exception.Message)"
    exit 6
}