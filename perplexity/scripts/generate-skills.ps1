# ============================================================
# generate-skills.ps1  v2.0
# Packager ZIP depuis perplexity/skills/*.md → ZIP à plat
# Règle 8 : les .md doivent être à la racine du ZIP (pas de sous-dossier)
# ============================================================
$ErrorActionPreference = "Stop"

$repoRoot   = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$skillsDir  = Join-Path $repoRoot "perplexity\skills"
$buildDir   = Join-Path $repoRoot "perplexity\build"
$zipPath    = Join-Path $buildDir "Skills.zip"

# Vérification source
if (-not (Test-Path $skillsDir)) {
    Write-Error "Dossier source introuvable : $skillsDir"
    exit 1
}

$files = Get-ChildItem -Path $skillsDir -Filter "*.md"
if ($files.Count -eq 0) {
    Write-Error "Aucun fichier .md dans $skillsDir"
    exit 1
}

Write-Host "  $($files.Count) skills trouves dans $skillsDir"

# Créer build/ si absent
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null

# Supprimer le ZIP précédent
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

# Copie à plat dans un temp (règle 8 : pas de sous-dossier dans le ZIP)
$tempDir = Join-Path $env:TEMP "SkillsZipTemp_$(Get-Random)"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

foreach ($f in $files) {
    Copy-Item $f.FullName -Destination (Join-Path $tempDir $f.Name)
}

# Compression à plat
Compress-Archive -Path (Join-Path $tempDir "*.md") -DestinationPath $zipPath -Force
Remove-Item $tempDir -Recurse -Force

# Résumé
$zipSize = (Get-Item $zipPath).Length
Write-Host "ZIP cree : $zipPath ($($files.Count) skills, $([math]::Round($zipSize/1024,1)) KB)"
Write-Host "Importer ce ZIP dans Perplexity > Space > Skills."
