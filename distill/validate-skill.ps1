#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Valide un candidat SKILL.md avant promotion vers skills/ (statut active).

.DESCRIPTION
    Porte de validation inspirée de skillforge et LearnKit.
    Contrôle un brouillon SKILL.md dans reviews/skill-drafts/ contre
    SPEC-SKILL-FORMAT.md et les règles de gouvernance (explicit-path-*, Preuve Fraîche,
    anti-doublon, sandbox). Uniquement les candidats validés passent en statut active.

.PARAMETER DraftPath
    Chemin vers le fichier SKILL.md candidat à valider (obligatoire).

.PARAMETER SkillsRoot
    Répertoire racine des skills actifs (défaut: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills).

.PARAMETER IndexPath
    Chemin vers skills-index.json pour détection de doublons (défaut:
    D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json).

.PARAMETER AutoPromote
    Si spécifié, promeut le skill vers skills/ après validation réussie (défaut: pas de promotion).

.PARAMETER BaseSkill
    Nom d'un skill existant dans skills/ à mettre à jour (fusion incrémentale). Si spécifié,
    le candidat est fusionné dans le skill existant avec incrément semver (v0.1.0 -> v0.1.1)
    au lieu de créer un nouveau dossier.

.EXAMPLE
    ./validate-skill.ps1 -DraftPath "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\reviews\skill-drafts\mon-skill\SKILL.md"

.EXAMPLE
    ./validate-skill.ps1 -DraftPath "..." -SkillsRoot "..." -AutoPromote

.EXAMPLE
    ./validate-skill.ps1 -DraftPath "..." -BaseSkill "mon-skill-existant"

.NOTES
    Intégration: D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\SPEC-SKILL-FORMAT.md (section 9, 10)
    Inspiration: skillforge (gate ≥3 cas vérifiés, pas de doublon, sandbox),
    LearnKit (quality-gated sur résultat outil réel).
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$DraftPath,

    [string]$SkillsRoot = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills",

    [string]$IndexPath = "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json",

    [switch]$AutoPromote,

    [string]$BaseSkill
)

$errors = @()
$warnings = @()
$nowUtc = (Get-Date).ToUniversalTime().ToString("o")

# --- Vérification pré-exécution des chemins (règle Explicit Path Compliance) ---
if (-not (Test-Path -LiteralPath $DraftPath)) {
    Write-Error "Fichier candidat introuvable : $DraftPath"
    exit 1
}

if (-not (Test-Path -LiteralPath $SkillsRoot)) {
    Write-Error "Répertoire skills introuvable : $SkillsRoot"
    exit 1
}

# --- Lecture du fichier candidat ---
$content = Get-Content -LiteralPath $DraftPath -Raw -ErrorAction Stop
# Nettoyer le BOM UTF-8 s'il est présent (Set-Content l'ajoute)
$content = $content -replace "^\xEF\xBB\xBF", ""
# Normaliser les fins de ligne (CRLF -> LF) pour les regex de sections
$content = $content -replace "`r`n", "`n"

function Test-YamlFrontmatter {
    param([string]$Content)
    $match = [regex]::Match($Content, '^---\s*\n.*?\n---', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    return $match.Success
}

function Extract-YamlValue {
    param([string]$Content, [string]$Key)
    $match = [regex]::Match($content, "(?m)^${key}:\s*(.+)$")
    if ($match.Success) { return $match.Groups[1].Value.Trim().Trim('"') }
    return $null
}

function Extract-YamlListSection {
    param([string]$Content, [string]$SectionKey)
    $lines = $content -split "`n"
    $inSection = $false
    $result = @()
    foreach ($line in $lines) {
        if ($line -match "(?m)^${SectionKey}:\s*$") {
            $inSection = $true
            continue
        }
        if ($inSection) {
            $matchItem = [regex]::Match($line, "^\s*-\s*(.+)$")
            if ($matchItem.Success) {
                $result += $matchItem.Groups[1].Value.Trim().Trim('"')
            } elseif ($line -match "^\S" -and $line -notmatch "^\s*-\s") {
                # Nouvelle clé de premier niveau, fin de section
                break
            } elseif ($line -match "^---") {
                # Fin du frontmatter YAML
                break
            }
        }
    }
    return $result
}

# --- 1. Présence du frontmatter YAML ---
if (-not (Test-YamlFrontmatter -Content $content)) {
    $errors += "FRONTMATTER_MISSING: Le fichier SKILL.md ne contient pas de frontmatter YAML délimité par ---"
}

# --- 2. Champs obligatoires du frontmatter ---
$mandatoryFields = @("name", "version", "status", "type", "category", "intent_hash", "provenance", "source_shard", "created_at", "updated_at", "author", "triggers", "anti_triggers", "weight", "prerequisites", "verification", "hash_sha256_evidence")
foreach ($field in $mandatoryFields) {
    $val = Extract-YamlValue -Content $content -Key $field
    if ($null -eq $val -or $val -eq "") {
        $errors += "MISSING_FIELD: Le champ '$field' est obligatoire dans le frontmatter."
    }
}

# --- 3. Statut doit être draft pour un candidat ---
$status = Extract-YamlValue -Content $content -Key "status"
if ($status -ne "draft") {
    $warnings += "STATUS_NOT_DRAFT: Le statut est '$status', attendu 'draft' pour un candidat non promu."
}

# --- 4. Sections obligatoires du corps ---
$mandatorySections = @("Objectif", "Localisation", "Fichiers du skill", "Prérequis", "Procédure", "Vérification", "Historique")
foreach ($section in $mandatorySections) {
    if ($content -notmatch "(?m)^## ${section}") {
        $errors += "MISSING_SECTION: La section '## $section' est obligatoire dans le corps du SKILL.md."
    }
}

# --- 5. Hash SHA-256 dans EVIDENCE.md (pas d'auto-référence dans SKILL.md) ---
$declaredHashEvidence = Extract-YamlValue -Content $content -Key "hash_sha256_evidence"
if ($null -eq $declaredHashEvidence -or $declaredHashEvidence -eq "" -or $declaredHashEvidence -like "*placeholder*") {
    $warnings += "HASH_EVIDENCE_PENDING: Le champ hash_sha256_evidence est absent ou placeholder. Il sera calculé dans EVIDENCE.md après première utilisation."
} else {
    # Vérifier que le hash n'est pas auto-référencé (pas de hash_sha256 dans le frontmatter)
    $oldHash = Extract-YamlValue -Content $content -Key "hash_sha256"
    if ($null -ne $oldHash -and $oldHash -ne "") {
        $errors += "HASH_AUTO_REFERENCE: Le champ hash_sha256 ne doit plus apparaître dans le frontmatter (auto-référence circulaire). Utilisez hash_sha256_evidence dans EVIDENCE.md à la place."
    }
}

# --- 6. Détection de doublon (anti-doublon, inspiré skillforge) ---
$skillName = Extract-YamlValue -Content $content -Key "name"
if (-not $skillName) {
    $skillName = Split-Path -Parent $DraftPath | Split-Path -Leaf
}

if (Test-Path -LiteralPath $IndexPath) {
    $indexContent = Get-Content -LiteralPath $IndexPath -Raw -ErrorAction SilentlyContinue
    if ($indexContent) {
        try {
            $index = $indexContent | ConvertFrom-Json -ErrorAction Stop
            foreach ($s in $index.skills) {
                if ($s.name -eq $skillName) {
                    $errors += "DUPLICATE_SKILL: Un skill actif nommé '$skillName' existe déjà dans l'index (chemin: $($s.skill_path)). Utilisez --base-skill pour mise à jour ou changez le nom."
                }
                if ($s.intent_hash -eq (Extract-YamlValue -Content $content -Key "intent_hash")) {
                    $warnings += "INTENT_HASH_SIMILAR: Un skill existant partage le même intent_hash ($($s.intent_hash)). Risque de doublon fonctionnel."
                }
            }
        } catch {
            $warnings += "INDEX_PARSE_ERROR: Impossible de parser skills-index.json pour détection de doublons."
        }
    }
}

# --- 7. Vérification des chemins (explicit-path-compliance / no-default-path-substitution) ---
# Chercher le chemin par défaut interdit (sans L4-TOOLS)
$forbiddenPaths = @("D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\")
foreach ($fp in $forbiddenPaths) {
    if ($content -match [regex]::Escape($fp)) {
        $errors += "FORBIDDEN_PATH: Le chemin par défaut '$fp' apparaît dans le SKILL.md. Utilisez le chemin explicite fourni par l'utilisateur (D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS)."
    }
}

# --- 8. Prérequis non vides ---
$prereqs = Extract-YamlListSection -Content $content -SectionKey "prerequisites"
if ($prereqs.Count -eq 0) {
    $warnings += "EMPTY_PREREQUISITES: Aucun prérequis déclaré. Ajoutez au moins un prérequis (port, fichier, variable d'environnement, processus résident)."
}

# --- 9. Vérification de la commande de vérification ---
$verifyCmd = Extract-YamlValue -Content $content -Key "verification.command"
if ($null -eq $verifyCmd -or $verifyCmd -eq "TODO - à définir après validation") {
    $warnings += "VERIFICATION_TODO: La commande de vérification n'est pas encore définie. À compléter avant promotion."
}

# --- 10. Validation syntaxique et d'existence des entrypoints (T004) ---
$entrypoints = Extract-YamlListSection -Content $content -SectionKey "entrypoints"
if ($entrypoints.Count -gt 0) {
    foreach ($ep in $entrypoints) {
        $epPath = Resolve-Path -LiteralPath $ep -ErrorAction SilentlyContinue
        if (-not $epPath) {
            $epPath = Join-Path $PSScriptRoot $ep
        }
        if (-not (Test-Path -LiteralPath $epPath)) {
            # Essayer depuis la racine du repo Skills (parent du dossier distill/)
            $repoRoot = Join-Path $PSScriptRoot ".."
            $epPath = Join-Path $repoRoot $ep
        }
        if (-not (Test-Path -LiteralPath $epPath)) {
            # Essayer depuis SkillsRoot (dossier skills/)
            $epPath = Join-Path $SkillsRoot $ep
        }
        if (-not (Test-Path -LiteralPath $epPath)) {
            $errors += "ENTRYPOINT_MISSING: L'entrypoint '$ep' n'existe pas sur ENV2."
        } else {
            # Contrôle syntaxique PowerShell si c'est un .ps1
            if ($epPath -like "*.ps1") {
                $epErrors = $null
                $null = [System.Management.Automation.Language.Parser]::ParseFile($epPath, [ref]$null, [ref]$epErrors)
                if ($epErrors) {
                    foreach ($e in $epErrors) {
                        $errors += "ENTRYPOINT_SYNTAX: $ep — $($e.Message)"
                    }
                } else {
                    $epBytes = [System.IO.File]::ReadAllBytes($epPath)
                    $sha256 = [System.Security.Cryptography.SHA256]::Create()
                    $hashBytes = $sha256.ComputeHash($epBytes)
                    $epHash = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ''
                    $warnings += "ENTRYPOINT_OK: $ep — hash SHA-256 $epHash"
                }
            }
        }
    }
}

# --- Rapport ---
Write-Output "=============================================="
Write-Output "Validation SKILL.md : $DraftPath"
Write-Output "=============================================="
Write-Output "Nom          : $skillName"
Write-Output "Statut       : $status"
Write-Output "Erreurs      : $($errors.Count)"
Write-Output "Avertissements: $($warnings.Count)"
Write-Output "=============================================="

if ($errors.Count -gt 0) {
    Write-Output "ERREURS BLOQUANTES :"
    foreach ($e in $errors) { Write-Output "  - $e" }
    Write-Output "=============================================="
    Write-Output "RESULTAT : REJETÉ — Corrigez les erreurs ci-dessus avant nouvelle tentative."
    exit 1
}

if ($warnings.Count -gt 0) {
    Write-Output "AVERTISSEMENTS :"
    foreach ($w in $warnings) { Write-Output "  - $w" }
    Write-Output "=============================================="
}

Write-Output "RESULTAT : VALIDE — Prêt pour promotion vers skills/ (statut: active)."

# --- Promotion optionnelle ou fusion incrémentale (T003) ---
if ($AutoPromote -or $BaseSkill) {
    if ($BaseSkill) {
        # --- T003 : Fusion incrémentale semver (v0.1.0 -> v0.1.1) ---
        $targetFolder = Join-Path $SkillsRoot $BaseSkill
        if (-not (Test-Path -LiteralPath $targetFolder)) {
            Write-Error "Le skill cible n'existe pas : $targetFolder. Fusion annulée."
            exit 1
        }
        $targetFile = Join-Path $targetFolder "SKILL.md"
        if (-not (Test-Path -LiteralPath $targetFile)) {
            Write-Error "SKILL.md introuvable dans $targetFolder. Fusion annulée."
            exit 1
        }
        $targetContent = Get-Content -LiteralPath $targetFile -Raw
        # Nettoyer BOM et normaliser
        $targetContent = $targetContent -replace "^\xEF\xBB\xBF", "" -replace "`r`n", "`n"
        $currentVersion = Extract-YamlValue -Content $targetContent -Key "version"
        if (-not $currentVersion -or $currentVersion -eq "") { $currentVersion = "0.0.0" }
        # Incrément semver patch : v0.1.0 -> v0.1.1
        $versionParts = $currentVersion.Trim('v') -split '\.'
        if ($versionParts.Count -ge 3) {
            $versionParts[2] = ([int]$versionParts[2] + 1).ToString()
        } elseif ($versionParts.Count -eq 2) {
            $versionParts += "1"
        } else {
            $versionParts = @("0", "0", "1")
        }
        $newVersion = "v$($versionParts[0]).$($versionParts[1]).$($versionParts[2])"
        $targetContent = $targetContent -replace '(?m)^version:.*$', "version: `"$newVersion`""
        $targetContent = $targetContent -replace '(?m)^status:.*$', "status: active"
        $targetContent = $targetContent -replace '(?m)^updated_at:.*$', "updated_at: `"$nowUtc`""
        # Fusion : ajouter les sections manquantes du candidat
        foreach ($section in $mandatorySections) {
            if ($targetContent -notmatch "(?m)^## ${section}") {
                $targetContent += "`n`n## $section`n`nÀ compléter depuis le candidat."
            }
        }
        Set-Content -LiteralPath $targetFile -Value $targetContent -Encoding UTF8
        # Mettre à jour HISTORY.md
        $historyFile = Join-Path $targetFolder "HISTORY.md"
        if (Test-Path -LiteralPath $historyFile) {
            $historyContent = Get-Content -LiteralPath $historyFile -Raw
            $historyEntry = "`n`n## $newVersion — $nowUtc`n- Fusion incrémentale depuis candidat $skillName (distillé).`n- Statut: active`
"
            $historyContent = $historyContent.TrimEnd() + $historyEntry
            Set-Content -LiteralPath $historyFile -Value $historyContent -Encoding UTF8
        }
        Write-Output "FUSION : Skill '$BaseSkill' mis à jour en version $newVersion (statut: active)."
        $skillName = $BaseSkill
    } elseif ($AutoPromote) {
        # --- T008 : Promotion atomique vers skills/ ---
        $targetFolder = Join-Path $SkillsRoot $skillName
        if (Test-Path -LiteralPath $targetFolder) {
            Write-Error "Le dossier cible existe déjà : $targetFolder. Utilisez -BaseSkill pour fusion incrémentale."
            exit 1
        }
        New-Item -ItemType Directory -Force -Path $targetFolder | Out-Null
        # Copier SKILL.md
        Copy-Item -LiteralPath $DraftPath -Destination (Join-Path $targetFolder "SKILL.md")
        # Mettre à jour le statut dans la copie
        $targetFile = Join-Path $targetFolder "SKILL.md"
        $targetContent = Get-Content -LiteralPath $targetFile -Raw
        $targetContent = $targetContent -replace '(?m)^status: draft$', "status: active"
        Set-Content -LiteralPath $targetFile -Value $targetContent -Encoding UTF8
        Write-Output "PROMOTION : Skill '$skillName' promu vers $targetFolder (statut: active)."
    # Créer HISTORY.md et EVIDENCE.md si absents (T008)
    $historyFile = Join-Path $targetFolder "HISTORY.md"
    if (-not (Test-Path -LiteralPath $historyFile)) {
        $historyContent = "# Historique des versions — $skillName`n`n## v0.1.0 — $nowUtc`n- Promotion initiale depuis `reviews/skill-drafts/`.`n- Statut: active"
        Set-Content -LiteralPath $historyFile -Value $historyContent -Encoding UTF8
    }
    $evidenceFile = Join-Path $targetFolder "EVIDENCE.md"
    if (-not (Test-Path -LiteralPath $evidenceFile)) {
        $evidenceContent = "# Preuve d'exécution — $skillName`n`nEn attente de première utilisation réussie.`nAucune preuve n'a encore été enregistrée."
        Set-Content -LiteralPath $evidenceFile -Value $evidenceContent -Encoding UTF8
    }
    }
    # Régénération automatique de l'index (règle de fraîcheur) (T009)
    $indexScript = Join-Path $PSScriptRoot "index-skills.ps1"
    if (Test-Path -LiteralPath $indexScript) {
        pwsh -File $indexScript -SkillsRoot $SkillsRoot -OutputPath $IndexPath | Out-Null
        Write-Output "INDEX : skills-index.json régénéré automatiquement après promotion/fusion."
    } else {
        Write-Output "ATTENTION : index-skills.ps1 introuvable à $indexScript. Régénérez manuellement skills-index.json."
    }
}

Write-Output "=============================================="

