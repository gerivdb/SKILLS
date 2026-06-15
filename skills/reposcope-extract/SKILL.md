---
name: reposcope-extract
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_EXTRACT_20260615
---

# Skill: reposcope-extract

## Quand l'utiliser

- L'utilisateur fournit une URL GitHub (`<owner>/<repo>`) et veut en extraire les dimensions clés
- Le pipeline REPOSCOPE-COMPARE nécessite un artefact d'extraction en entrée
- ECOS-CLI `reposcope-extract <url>` est appelé

**NE PAS utiliser** pour l'analyse de code source local (utiliser `reposcope-run` à la place).

## Références

- **INTENT** : INTENT-041a (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-EXTRACTOR-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-EXTRACTOR
- **Schéma de sortie** : `extraction` (YAML)

## Pipeline d'extraction

### Étape 1 — Valider l'entrée

```powershell
# Vérifier que l'URL est bien formatée
if ($url -notmatch '^[\w-]+/[\w-]+$') {
    Write-Output "[ERROR] URL invalide. Format attendu: <owner>/<repo>"
    exit 1
}
```

### Étape 2 — Appels GitHub API

```powershell
# Base URL
$base = "https://api.github.com/repos/$url"

# 1. Métadonnées principales
$repo = Invoke-RestMethod -Uri $base -Headers @{Accept = "application/vnd.github.v3+json"}

# 2. Langages
$langs = Invoke-RestMethod -Uri "$base/languages" -Headers @{Accept = "application/vnd.github.v3+json"}

# 3. Topics
$topicsResp = Invoke-RestMethod -Uri "$base/topics" -Headers @{Accept = "application/vnd.github.mercy-preview+json"}
$topics = $topicsResp.names

# 4. Arborescence niveau 1
$tree = Invoke-RestMethod -Uri "$base/git/trees/main?recursive=1" -Headers @{Accept = "application/vnd.github.v3+json"}
$dirs = $tree.tree | Where-Object { $_.type -eq "tree" } | Select-Object -First 20 path

# 5. README (tronqué)
$readme = Invoke-RestMethod -Uri "$base/readme" -Headers @{Accept = "application/vnd.github.v3+json"}
$readmeContent = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($readme.content)).Substring(0, [Math]::Min(2000, $readmeContent.Length))
```

### Étape 3 — Classification technique

```powershell
# Détection frameworks via fichiers de config détectés dans le tree
$frameworks = @()
$configFiles = $tree.tree.path | Where-Object { $_ -match "(package\.json|Cargo\.toml|requirements\.txt|go\.mod|pom\.xml|build\.gradle|pyproject\.toml|Gemfile)" }

if ($configFiles -match "package\.json") { $frameworks += "node" }
if ($configFiles -match "Cargo\.toml") { $frameworks += "rust" }
if ($configFiles -match "requirements\.txt|pyproject\.toml") { $frameworks += "python" }
if ($configFiles -match "go\.mod") { $frameworks += "go" }

# Pattern architectural
$pattern = "unknown"
$paths = ($tree.tree.path -join " ")
if ($paths -match "packages/|services/|apps/") { $pattern = "monorepo" }
elseif ($paths -match "Dockerfile" -and $paths -match "docker-compose") { $pattern = "microservice" }
elseif ($paths -match "lib/|src/" -and $paths -notmatch "main\.go|main\.py|index\.js") { $pattern = "library" }
elseif ($paths -match "cmd/|bin/|main\.go|main\.py") { $pattern = "cli" }
elseif ($paths -match "frontend/|ui/|static/") { $pattern = "webapp" }

# Maturité score [0.0-1.0]
$starsScore = [Math]::Min($repo.stargazers_count / 100, 1.0) * 0.3
$recency = if ($repo.updated_at -gt (Get-Date).AddMonths(-3)) { 1.0 } elseif ($repo.updated_at -gt (Get-Date).AddYears(-1)) { 0.5 } else { 0.2 }
$recencyScore = $recency * 0.4
$issuesScore = if ($repo.open_issues_count -lt 10) { 1.0 } elseif ($repo.open_issues_count -lt 50) { 0.6 } else { 0.3 }
$issuesScore *= 0.3
$maturity = [Math]::Round($starsScore + $recencyScore + $issuesScore, 3)
```

### Étape 4 — Classification architecturale

```powershell
# Mapping topics → strate L0→L9
$stratMap = @{
    "governance" = "L0_CONSTITUTIONAL"; "constitution" = "L0_CONSTITUTIONAL"
    "ontology" = "L1_CAUSALITY"; "causality" = "L1_CAUSALITY"; "semantic" = "L1_CAUSALITY"
    "cognitive" = "L3_EMERGENCE"; "ai" = "L3_EMERGENCE"; "ml" = "L3_EMERGENCE"; "llm" = "L3_EMERGENCE"
    "tooling" = "L4_DEVTOOLS"; "devtools" = "L4_DEVTOOLS"; "cli" = "L4_DEVTOOLS"
    "citizen" = "L3_CITIZENS"; "agent" = "L3_CITIZENS"
    "infrastructure" = "L1_INFRA"; "runtime" = "L1_INFRA"
    "documentation" = "L2_COMPOSITION"; "docs" = "L2_COMPOSITION"
}

$inferredStrata = @()
foreach ($topic in $topics) {
    $key = $topic.ToLower()
    if ($stratMap.ContainsKey($key) -and $inferredStrata -notcontains $stratMap[$key]) {
        $inferredStrata += $stratMap[$key]
    }
}

# Inférence rôle Trit
$tritRole = "E"
if ($repo.description -match "governance|registry|policy|standard") { $tritRole = "C" }
if ($repo.description -match "monitor|analytics|observe|observab") { $tritRole = "Obs" }
```

### Étape 5 — Sortie YAML

```powershell
$extraction = @{
    extraction = @{
        source = $url
        extracted_at = (Get-Date -Format "o")
        version = "1.0"
        semantic = @{
            description = $repo.description
            topics = @()
            languages = @{}
            readme_summary = ""
            tree_depth_1 = @()
        }
        technical = @{
            frameworks = @()
            architecture_pattern = "unknown"
            maturity_score = 0.0
        }
        architectural = @{
            inferred_strata = @()
            inferred_trit_role = "E"
        }
    }
}

# Peupler les données
$extraction.extraction.semantic.topics = $topics
$extraction.extraction.semantic.languages = $langs
$extraction.extraction.semantic.readme_summary = $readmeContent
$extraction.extraction.semantic.tree_depth_1 = $dirs
$extraction.extraction.technical.frameworks = $frameworks
$extraction.extraction.technical.architecture_pattern = $pattern
$extraction.extraction.technical.maturity_score = $maturity
$extraction.extraction.architectural.inferred_strata = $inferredStrata
$extraction.extraction.architectural.inferred_trit_role = $tritRole

# Écrire le YAML
$yaml = $extraction | ConvertTo-Yaml -Depth 10
$slug = $url.Replace("/", "_")
$outputPath = "NEXUS/reposcope/extract_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
$yaml | Out-File -FilePath $outputPath -Encoding UTF8
Write-Output "[reposcope-extract] Artefact ecrit: $outputPath"
Write-Output $yaml
```

## Gestion d'erreurs

| Erreur | HTTP Code | Action |
|---|---|---|
| Repo inexistant | 404 | `Write-Output "[ERROR] Repo introuvable: $url"` + exit 1 |
| Rate limit | 403 | Lire `Retry-After` header, attendre, retry (max 3) |
| Timeout | — | 30s timeout sur chaque appel API |
| README inaccessible | 404 | Ignorer (readme_summary = "") |
| Pas de tree `main` | 404 | Essayer `master`, puis `HEAD` |

## Critères de succès

- [ ] YAML valide produit pour tout repo GitHub accessible
- [ ] Toutes les 3 dimensions peuplées (même partiellement)
- [ ] Timeout < 30s par repo
- [ ] Gestion erreurs 404/403/timeout

## Skills liés

- **reposcope-score** : consume l'artefact d'extraction pour le scoring
- **reposcope-compare** : orchestre le pipeline complet
