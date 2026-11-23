#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Protocole de phagocytose profonde sur ENV2.

.DESCRIPTION
    Implémente les 5 étapes de phagocytose définies dans PHAGOCYTOSE-SPEC.md :
    1. Capture fidèle de la source ou du transcript (T033)
    2. Déconstruction et tri anti-bruit (T034)
    3. Normalisation au format canonique SKILL.md (T035)
    4. Validation & garde-fou (appel validate-skill.ps1) (T036)
    5. Indexation & réactivation (appel index-skills.ps1) (T037)

.PARAMETER SourcePath
    Chemin vers la source à phagocyter (fichier transcript, script, ou extrait de dépôt).

.PARAMETER SourceName
    Nom de la source (servira de base au nom du skill). Si omis, dérivé du nom de fichier.

.PARAMETER SourceUrl
    URL ou chemin d'origine de la source (pour traçabilité).

.PARAMETER CapturesDir
    Répertoire où stocker les captures brutes (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\captures).

.PARAMETER DraftsDir
    Répertoire où créer le SKILL.md candidat (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\reviews\skill-drafts).

.PARAMETER ArchivesDir
    Répertoire d'archivage des sources phagocytées (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\archives).

.PARAMETER ValidateOnly
    Si spécifié, ne fait que valider un skill déjà existant sans relancer la phagocytose complète.

.EXAMPLE
    ./phagocytose.ps1 -SourcePath "C:\Users\GG\session-transcript.jsonl" -SourceName "cdp-profile-2" -SourceUrl "https://gemini.google.com/app/ef4a2ac1b3b96dca"

.EXAMPLE
    ./phagocytose.ps1 -SourcePath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\distill-skill.ps1" -SourceName "distill-skill"

.NOTES
    Intégration: PHAGOCYTOSE-SPEC.md (Phase 4, T031-T040)
    Dépend: validate-skill.ps1, index-skills.ps1
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePath,

    [string]$SourceName,

    [string]$SourceUrl,

    [string]$CapturesDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\captures",

    [string]$DraftsDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\reviews\skill-drafts",

    [string]$ArchivesDir = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\phagocytose\archives",

    [switch]$ValidateOnly
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution du chemin (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $SourcePath)) {
    Write-Error "Source introuvable : $SourcePath"
    exit 1
}

if (-not $SourceName) {
    $SourceName = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
    $SourceName = $SourceName -replace '[^a-z0-9\-]', '-' -replace '-+', '-'
    $SourceName = $SourceName.Trim('-')
}

# --- ÉTAPE 1 : Capture fidèle (T033) ---
Write-Output "=============================================="
Write-Output "PHAGOCYTOSE — Étape 1 : Capture fidèle"
Write-Output "=============================================="

if (-not (Test-Path -LiteralPath $CapturesDir)) {
    New-Item -ItemType Directory -Force -Path $CapturesDir | Out-Null
}

$captureFileName = "$($SourceName)-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ')).capture"
$capturePath = Join-Path $CapturesDir $captureFileName

$sourceContent = Get-Content -LiteralPath $SourcePath -Raw -ErrorAction Stop
$sourceBytes = [System.IO.File]::ReadAllBytes($SourcePath)
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$hashBytes = $sha256.ComputeHash($sourceBytes)
$sourceHash = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''

$captureContent = @()
$captureContent += "=== CAPTURE PHAGOCYTOSE ==="
$captureContent += "Date UTC : $nowUtc"
$captureContent += "Source   : $SourcePath"
$captureContent += "URL      : $SourceUrl"
$captureContent += "Hash SHA-256 brut : $sourceHash"
$captureContent += "Taille   : $($sourceBytes.Length) octets"
$captureContent += "=== CONTENU BRUT ==="
$captureContent += $sourceContent

$captureContent -join "`n" | Set-Content -LiteralPath $capturePath -Encoding UTF8

Write-Output "Capture créée : $capturePath"
Write-Output "Hash SHA-256  : $sourceHash"

# --- ÉTAPE 2 : Déconstruction et tri anti-bruit (T034) ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE — Étape 2 : Déconstruction et tri anti-bruit"
Write-Output "=============================================="

# Analyser le contenu pour extraire :
# - Faits vérifiés (commandes exécutées avec succès, tests passés)
# - Hypothèses (commentaires spéculatifs, TODO)
# - Dépendances (imports, require, using, #include)
# - Étapes reproductibles (séquences de commandes)

$factsVerifies = @()
$hypotheses = @()
$dependances = @()
$etapesReproductibles = @()

$lignes = $sourceContent -split "`n"
foreach ($ligne in $lignes) {
    $trimmed = $ligne.Trim()
    if (-not $trimmed) { continue }

    # Détection dépendances (imports, requires, includes, modules)
    if ($trimmed -match '(?i)(^|\s)(import|require|include|using|module|from|package)\s+') {
        $dependances += $trimmed
    }
    # Détection hypothèses (TODO, FIXME, XXX, ?, peut-être, supposons)
    elseif ($trimmed -match '(?i)(TODO|FIXME|XXX|\?|peut.être|supposons|à vérifier|en attente)') {
        $hypotheses += $trimmed
    }
    # Détection faits vérifiés (commandes, tests, code de retour, succès)
    elseif ($trimmed -match '(?i)(code de retour|exit code|succès|success|testé|validé|fonctionne|operational|OK$)') {
        $factsVerifies += $trimmed
    }
    # Détection étapes reproductibles (numérotées, flèches, ->, étape)
    elseif ($trimmed -match '(?i)(étape|step|->|=>|1\.|2\.|3\.)') {
        $etapesReproductibles += $trimmed
    }
}

$deconstruction = [PSCustomObject]@{
    date_utc = $nowUtc
    source = $SourcePath
    source_hash = $sourceHash
    faits_verifies = @($factsVerifies)
    hypotheses = @($hypotheses)
    dependances = @($dependances)
    etapes_reproductibles = @($etapesReproductibles)
}

$deconstructionJson = $deconstruction | ConvertTo-Json -Depth 3
$deconstructionPath = Join-Path $CapturesDir "$($SourceName)-deconstruction.json"
$deconstructionJson | Set-Content -LiteralPath $deconstructionPath -Encoding UTF8

Write-Output "Faits vérifiés      : $($factsVerifies.Count)"
Write-Output "Hypothèses          : $($hypotheses.Count)"
Write-Output "Dépendances         : $($dependances.Count)"
Write-Output "Étapes reproductibles: $($etapesReproductibles.Count)"
Write-Output "Déconstruction      : $deconstructionPath"

# --- ÉTAPE 3 : Normalisation au format canonique (T035) ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE — Étape 3 : Normalisation canonique"
Write-Output "=============================================="

$skillName = $SourceName
$skillDir = Join-Path $DraftsDir $skillName
$skillFile = Join-Path $skillDir "SKILL.md"

if (Test-Path -LiteralPath $skillFile) {
    Write-Error "Un skill existe déjà : $skillFile"
    exit 1
}

$intentHash = "0x" + ($skillName.ToUpper() + "_" + $nowUtc.Substring(0,10).Replace("-",""))

# Déduire les triggers depuis le nom et le contenu
$triggers = @($skillName.Split('-'))
if ($sourceContent -match '(?i)chromium') { $triggers += "chromium" }
if ($sourceContent -match '(?i)cdp') { $triggers += "cdp" }
if ($sourceContent -match '(?i)profile') { $triggers += "profile" }
if ($sourceContent -match '(?i)git') { $triggers += "git" }
if ($sourceContent -match '(?i)python') { $triggers += "python" }
if ($sourceContent -match '(?i)9222') { $triggers += "9222" }
$triggers = $triggers | Select-Object -Unique

# Déduire les anti_triggers
$antiTriggers = @()
if ($sourceContent -match '(?i)headless') { $antiTriggers += "headless" }
if ($sourceContent -match '(?i)profil.?temporaire') { $antiTriggers += "profil temporaire" }
if ($sourceContent -match '(?i)shard-?env6') { $antiTriggers += "shard-ENV6" }

# Déduire les poids (premier trigger le plus important)
$weights = @()
$wCount = 0
foreach ($t in $triggers) {
    $weights += (5 - $wCount)
    $wCount++
}
if ($weights.Count -eq 0) { $weights += 1 }

# Prérequis déduits
$prerequisites = @("PowerShell 7+")
if ($dependances.Count -gt 0) {
    $prerequisites += "Dépendances détectées : $($dependances -join ', ')"
}

$frontmatterLines = @()
$frontmatterLines += "---"
$frontmatterLines += "name: $skillName"
$frontmatterLines += 'version: "0.1.0"'
$frontmatterLines += "status: draft"
$frontmatterLines += "type: procedural"
$frontmatterLines += "category: phagocytose"
$frontmatterLines += "intent_hash: $intentHash"
$frontmatterLines += "provenance: phagocytose"
$frontmatterLines += "source_shard: ENV2"
$frontmatterLines += "created_at: `"$nowUtc`""
$frontmatterLines += "updated_at: `"$nowUtc`""
$frontmatterLines += "author: auto"
$frontmatterLines += "triggers:"
foreach ($t in $triggers) {
    $frontmatterLines += "  - `"$t`""
}
$frontmatterLines += "anti_triggers:"
foreach ($at in $antiTriggers) {
    $frontmatterLines += "  - `"$at`""
}
$frontmatterLines += "weight:"
foreach ($w in $weights) {
    $frontmatterLines += "  - $w"
}
$frontmatterLines += "prerequisites:"
foreach ($p in $prerequisites) {
    $frontmatterLines += "  - `"$p`""
}
$frontmatterLines += "verification:"
$frontmatterLines += '  command: "TODO - à définir après validation"'
$frontmatterLines += "  expected_exit_code: 0"
$frontmatterLines += '  expected_output_contains: "TODO"'
$frontmatterLines += 'hash_sha256_evidence: "placeholder - à remplir dans EVIDENCE.md après première utilisation"'
$frontmatterLines += "supersedes: []"
$frontmatterLines += "superseded_by: null"
$frontmatterLines += "tags:"
$frontmatterLines += '  - "phagocytose"'
$frontmatterLines += '  - "shard-ENV2"'
$frontmatterLines += "---"

$bodyLines = @()
$bodyLines += ""
$bodyLines += "# Skill : $skillName — Phagocytose depuis $SourcePath"
$bodyLines += ""
$bodyLines += "## Objectif"
$bodyLines += "Skill produit par phagocytose profonde de la source : $SourcePath"
$bodyLines += ""
$bodyLines += "## Localisation"
$bodyLines += "`$skillDir"
$bodyLines += ""
$bodyLines += "## Fichiers du skill"
$bodyLines += "- `SKILL.md` — ce document (généré par phagocytose.ps1)."
$bodyLines += "- `EVIDENCE.md` — preuve d'exécution (créée après première utilisation)."
$bodyLines += "- `HISTORY.md` — journal des versions."
$bodyLines += ""
$bodyLines += "## Prérequis"
foreach ($p in $prerequisites) {
    $bodyLines += "- $p"
}
$bodyLines += ""
$bodyLines += "## Procédure"
$bodyLines += "Ce skill a été produit par phagocytose profonde. Les étapes ci-dessous sont extraites de la déconstruction."
$bodyLines += ""
if ($etapesReproductibles.Count -gt 0) {
    $bodyLines += "### Étapes reproductibles identifiées"
    foreach ($e in $etapesReproductibles) {
        $bodyLines += "- $e"
    }
    $bodyLines += ""
}
$bodyLines += "## Règles de bonne pratique"
$bodyLines += "- Valider chaque étape extraite avant promotion."
$bodyLines += "- Ne pas committer un skill phagocyté sans vérification manuelle."
$bodyLines += "- Respecter la règle Explicit Path Compliance pour tous les chemins."
$bodyLines += ""
$bodyLines += "## Vérification"
$bodyLines += "- Exécuter `validate-skill.ps1` sur ce candidat avant promotion."
$bodyLines += "- Tester la procédure décrite dans un shard cible (ENV2 ou ENV3)."
$bodyLines += ""
$bodyLines += "## Historique"
$bodyLines += "- v0.1.0 : Phagocytose depuis $SourcePath le $nowUtc (statut: draft)."
$bodyLines += "- Voir `HISTORY.md` après promotion vers `active`."

$fullContent = ($frontmatterLines + $bodyLines -join "`n")

New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
Set-Content -LiteralPath $skillFile -Value $fullContent -Encoding UTF8

# Recalculer le hash SHA-256 du fichier écrit
$fileBytes = [System.IO.File]::ReadAllBytes($skillFile)
$hashBytes = $sha256.ComputeHash($fileBytes)
$skillHash = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''

# Mettre à jour le hash dans le frontmatter
$content = Get-Content -LiteralPath $skillFile -Raw
$content = $content -replace 'hash_sha256_evidence: "placeholder - à remplir dans EVIDENCE.md après première utilisation"', "hash_sha256_evidence: `"$skillHash`""
Set-Content -LiteralPath $skillFile -Value $content -Encoding UTF8

# Créer HISTORY.md et EVIDENCE.md
$historyFile = Join-Path $skillDir "HISTORY.md"
$historyContent = "# Historique des versions — $skillName`n`n## v0.1.0 — $nowUtc`n- Création par phagocytose depuis $SourcePath`n- Statut: draft"
Set-Content -LiteralPath $historyFile -Value $historyContent -Encoding UTF8

$evidenceFile = Join-Path $skillDir "EVIDENCE.md"
$evidenceContent = "# Preuve d'exécution — $skillName`n`nEn attente de première utilisation réussie.`nAucune preuve n'a encore été enregistrée."
Set-Content -LiteralPath $evidenceFile -Value $evidenceContent -Encoding UTF8

Write-Output "SKILL.md créé : $skillFile"
Write-Output "Hash SHA-256  : $skillHash"

# --- ÉTAPE 4 : Validation & garde-fou (T036) ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE — Étape 4 : Validation & garde-fou"
Write-Output "=============================================="

$validateScript = Join-Path (Split-Path -Parent $PSScriptRoot) "validate-skill.ps1"
if (-not (Test-Path -LiteralPath $validateScript)) {
    # Essayer depuis le dossier distill/
    $validateScript = Join-Path $PSScriptRoot "validate-skill.ps1"
}

if (Test-Path -LiteralPath $validateScript) {
    $validateResult = pwsh -File $validateScript -DraftPath $skillFile -SkillsRoot "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills" -IndexPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json"
    $validateResult | Write-Output
    $lastExitCode = $LASTEXITCODE
    if ($lastExitCode -ne 0) {
        $errors += "VALIDATION_ECHEC: validate-skill.ps1 a retourné un code de sortie non nul ($lastExitCode)."
    }
} else {
    $warnings += "VALIDATION_SKIPPED: validate-skill.ps1 introuvable à $validateScript."
}

# --- ÉTAPE 5 : Indexation & réactivation (T037) ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE — Étape 5 : Indexation & réactivation"
Write-Output "=============================================="

$indexScript = Join-Path (Split-Path -Parent $PSScriptRoot) "index-skills.ps1"
if (-not (Test-Path -LiteralPath $indexScript)) {
    $indexScript = Join-Path $PSScriptRoot "index-skills.ps1"
}

if (Test-Path -LiteralPath $indexScript) {
    $indexResult = pwsh -File $indexScript -SkillsRoot "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS" -OutputPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json"
    $indexResult | Write-Output
} else {
    $warnings += "INDEXATION_SKIPPED: index-skills.ps1 introuvable à $indexScript."
}

# --- ÉTAPE T039 : Archivage de la source phagocytée ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE — Étape T039 : Archivage de la source"
Write-Output "=============================================="

if (-not (Test-Path -LiteralPath $ArchivesDir)) {
    New-Item -ItemType Directory -Force -Path $ArchivesDir | Out-Null
}

$archiveDir = Join-Path $ArchivesDir "$($SourceName)-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmssZ'))"
New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

# Copier la capture brute
Copy-Item -LiteralPath $capturePath -Destination (Join-Path $archiveDir "capture.brut") | Out-Null
# Copier la déconstruction
Copy-Item -LiteralPath $deconstructionPath -Destination (Join-Path $archiveDir "deconstruction.json") | Out-Null
# Copier le SKILL.md final
Copy-Item -LiteralPath $skillFile -Destination (Join-Path $archiveDir "SKILL.md") | Out-Null

# Calculer les hashs des fichiers archivés
$archiveFiles = Get-ChildItem -LiteralPath $archiveDir -File
$archiveHashes = @()
foreach ($f in $archiveFiles) {
    $fBytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $fHash = ($sha256.ComputeHash($fBytes) | ForEach-Object { $_.ToString("x2") }) -join ''
    $archiveHashes += [PSCustomObject]@{ fichier = $f.Name; hash_sha256 = $fHash }
}

$archiveManifest = [PSCustomObject]@{
    date_utc = $nowUtc
    source = $SourcePath
    source_url = $SourceUrl
    source_hash = $sourceHash
    archive_dir = $archiveDir
    fichiers = $archiveHashes
}

$archiveManifest | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $archiveDir "manifest.json") -Encoding UTF8

Write-Output "Archive créée : $archiveDir"

# --- Rapport final ---
Write-Output "`n=============================================="
Write-Output "PHAGOCYTOSE TERMINÉE"
Write-Output "=============================================="
Write-Output "Source        : $SourcePath"
Write-Output "Skill         : $skillName"
Write-Output "Statut        : draft (en attente de validation manuelle si nécessaire)"
Write-Output "Capture       : $capturePath"
Write-Output "Déconstruction: $deconstructionPath"
Write-Output "SKILL.md      : $skillFile"
Write-Output "Archive       : $archiveDir"
Write-Output "Hash SHA-256  : $skillHash"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    Write-Output "ERREURS :"
    foreach ($e in $errors) { Write-Output "  - $e" }
    exit 1
}

if ($warnings.Count -gt 0) {
    Write-Output "AVERTISSEMENTS :"
    foreach ($w in $warnings) { Write-Output "  - $w" }
}
