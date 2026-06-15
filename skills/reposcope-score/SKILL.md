---
name: reposcope-score
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_SCORE_20260615
---

# Skill: reposcope-score

## Quand l'utiliser

- Un artefact d'extraction YAML (produit par `reposcope-extract`) est disponible
- Le pipeline REPOSCOPE-COMPARE nécessite un scoring multi-échelle
- ECOS-CLI `reposcope-score --input <extract.yaml>` est appelé

**NE PAS utiliser** sans un artefact d'extraction valide en entrée.

## Références

- **INTENT** : INTENT-041b (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-SCORING-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-SCORING
- **Schéma de sortie** : `scoring` (YAML)

## Sources de vérité requises

| Fichier | Chemin GOVERNANCE-HUB | Usage |
|---|---|---|
| `known_repositories.yaml` | `known_repositories.yaml` | Registre canonique 181 repos |
| `OrgansRegistry.yaml` | `OrgansRegistry.yaml` | Organes fonctionnels |
| `BRIDGES.yaml` | `BRIDGES.yaml` | Liens inter-repos |
| `TritRegistry.yaml` | `TritRegistry.yaml` | Logique ternaire C/E/Obs |

## Pipeline de scoring

### Étape 1 — Charger l'extraction + SOT

```powershell
# Charger l'artefact d'extraction
$extract = Get-Content $InputPath | ConvertFrom-Yaml

# Charger les SOT (cache si déjà chargé)
if (-not $global:KNOWN_REPOS) {
    $global:KNOWN_REPOS = Get-Content "GOVERNANCE-HUB/known_repositories.yaml" | ConvertFrom-Yaml
}
if (-not $global:ORGANS) {
    $global:ORGANS = Get-Content "GOVERNANCE-HUB/OrgansRegistry.yaml" | ConvertFrom-Yaml
}
```

### Étape 2 — Scoring MACRO (vue cluster)

```powershell
$allRepos = $global:KNOWN_REPOS.P0_CONSTITUTIONAL + $global:KNOWN_REPOS.P1_OPERATIONAL +
            $global:KNOWN_REPOS.P2_COMPOSITION + $global:KNOWN_REPOS.P3_EMERGENCE +
            $global:KNOWN_REPOS.P4_DEVTOOLS + $global:KNOWN_REPOS.P5_CITIZENS
$totalRepos = $allRepos.Count

# Calculer coverage par strate
$stratCoverage = @{}
foreach ($repo in $allRepos) {
    $layer = $repo.layer
    if (-not $stratCoverage.ContainsKey($layer)) {
        $stratCoverage[$layer] = 0
    }
    $stratCoverage[$layer]++
}

# Gap et uniqueness
$extStrata = $extract.extraction.architectural.inferred_strata
$targetStrate = if ($extStrata.Count -gt 0) { $extStrata[0] } else { "UNKNOWN" }
$coverage = if ($stratCoverage.ContainsKey($targetStrate)) { $stratCoverage[$targetStrate] / $totalRepos } else { 0 }
$gap = [Math]::Round(1.0 - $coverage, 3)

# Unicité : combien de repos gerivdb couvrent le même domaine
$matchingRepos = $allRepos | Where-Object { $_.role -match ($extract.extraction.semantic.topics -join "|") }
$uniqueness = [Math]::Round(1.0 - ($matchingRepos.Count / $totalRepos), 3)

$macro = @{
    strata_target = $targetStrate
    cluster_coverage_gap = $gap
    uniqueness_score = $uniqueness
}
```

### Étape 3 — Scoring MESO (vue organe)

```powershell
$mesoMatches = @()
foreach ($organ in $global:ORGANS.organs) {
    # Jaccard similarity sur les topics
    $organTopics = @($organ.name.ToLower()) + @($organ.proteins -replace '\.workflow$', '' | ForEach-Object { $_.ToLower() })
    $extTopics = $extract.extraction.semantic.topics | ForEach-Object { $_.ToLower() }
    $intersection = ($organTopics | Where-Object { $extTopics -contains $_ }).Count
    $union = ($organTopics + $extTopics | Select-Object -Unique).Count
    $jaccard = if ($union -gt 0) { [Math]::Round($intersection / $union, 3) } else { 0.0 }

    # Trit compatibility
    $extTrit = $extract.extraction.architectural.inferred_trit_role
    $tritCompat = if ($organ.name -match $extTrit) { 1.0 } else { 0.3 }

    $mesoScore = [Math]::Round(0.6 * $jaccard + 0.4 * $tritCompat, 3)

    $mesoMatches += @{
        organ = $organ.name
        score = $mesoScore
        trit_alignment = $extTrit
    }
}
```

### Étape 4 — Scoring ATOMIQUE (vue repo-à-repo)

```powershell
$atomicScores = @()
foreach ($gerivdbRepo in $allRepos) {
    # Semantic similarity (Jaccard topics)
    $gerivdbTopics = @($gerivdbRepo.role.ToLower()) + @($gerivdbRepo.name.ToLower())
    $extTopics = $extract.extraction.semantic.topics | ForEach-Object { $_.ToLower() }
    $semIntersection = ($gerivdbTopics | Where-Object { $extTopics -contains $_ }).Count
    $semUnion = ($gerivdbTopics + $extTopics | Select-Object -Unique).Count
    $simSemantic = if ($semUnion -gt 0) { [Math]::Round($semIntersection / $semUnion, 3) } else { 0.0 }

    # Technical similarity
    $simTechnical = if ($extract.extraction.technical.frameworks -contains $gerivdbRepo.technology) { 0.8 } else { 0.1 }

    # Architectural similarity
    $simArch = if ($gerivdbRepo.layer -eq $targetStrate) { 1.0 } elseif ($gerivdbRepo.layer -match $targetStrate.Split('_')[0]) { 0.5 } else { 0.0 }

    # Maturity similarity
    $extMaturity = $extract.extraction.technical.maturity_score
    $gerivdbMaturity = if ($gerivdbRepo.phi_cps) { [Math]::Min($gerivdbRepo.phi_cps / 5.0, 1.0) } else { 0.5 }
    $simMaturity = [Math]::Round(1.0 - [Math]::Abs($extMaturity - $gerivdbMaturity), 3)

    # φ-delta composite
    $weights = @{ semantic = 0.35; technical = 0.25; architectural = 0.25; maturity = 0.15 }
    $phiDelta = [Math]::Round(
        $weights.semantic * $simSemantic +
        $weights.technical * $simTechnical +
        $weights.architectural * $simArch +
        $weights.maturity * $simMaturity,
        3
    )

    # Classification
    $classification = "neutre"
    if ($phiDelta -gt 0.5 -and $simArch -gt 0.5) { $classification = "collision" }
    elseif ($phiDelta -ge 0.3) { $classification = "synergie" }

    $atomicScores += @{
        repo = $gerivdbRepo.full_name
        score = $phiDelta
        classification = $classification
        dimensions = @{
            semantic = $simSemantic
            technical = $simTechnical
            architectural = $simArch
            maturity = $simMaturity
        }
    }
}

# Trier par score décroissant
$top20 = $atomicScores | Sort-Object { $_.score } -Descending | Select-Object -First 20
```

### Étape 5 — Sortie YAML

```powershell
$scoring = @{
    scoring = @{
        source = $extract.extraction.source
        scored_at = (Get-Date -Format "o")
        version = "1.0"
        macro = $macro
        meso = $mesoMatches | Sort-Object { $_.score } -Descending
        atomic = @{
            top_20 = $top20
            full_count = $atomicScores.Count
            above_threshold_03 = ($atomicScores | Where-Object { $_.score -ge 0.3 }).Count
            above_threshold_05 = ($atomicScores | Where-Object { $_.score -ge 0.5 }).Count
        }
    }
}

$yaml = $scoring | ConvertTo-Yaml -Depth 10
$slug = $extract.extraction.source.Replace("/", "_")
$outputPath = "NEXUS/reposcope/score_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
$yaml | Out-File -FilePath $outputPath -Encoding UTF8
Write-Output "[reposcope-score] Artefact ecrit: $outputPath"
Write-Output "[reposcope-score] Top 5 repos:"
$top20 | Select-Object -First 5 | ForEach-Object { Write-Output "  $($_.repo): $($_.score) ($($_.classification))" }
```

## Gestion d'erreurs

| Erreur | Action |
|---|---|
| Artefact d'extraction invalide | `Write-Output "[ERROR] Artefact invalide: $InputPath"` + exit 1 |
| SOT manquant | `Write-Output "[ERROR] Fichier SOT introuvable"` + exit 2 |
| YAML mal formé | Capturer exception, afficher ligne erreur |

## Critères de succès

- [ ] Chaque strate a un score de gap
- [ ] Chaque organe a un score de projection
- [ ] Top-20 repos triés par φ-delta décroissant
- [ ] Classification collision/synergie/neutre correcte
- [ ] Exécution < 60s pour 181 repos

## Skills liés

- **reposcope-extract** : produit l'artefact d'extraction en entrée
- **reposcope-propagate** : consume le scoring pour la propagation
- **reposcope-compare** : orchestre le pipeline complet
