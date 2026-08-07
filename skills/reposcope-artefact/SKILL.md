---
name: reposcope-artefact
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_ARTEFACT_20260615
---

# Skill: reposcope-artefact

## Quand l'utiliser

- Les artefacts d'extraction, de scoring et de propagation sont disponibles
- Le pipeline REPOSCOPE-COMPARE necessite la generation de l'artefact final
- ECOS-CLI `reposcope-artefact` est appele avec les chemins des 3 artefacts

**NE PAS utiliser** sans les 3 artefacts d'entree valides.

## References

- **INTENT** : INTENT-041d (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-ARTEFACT-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-ARTEFACT

## Pipeline d'artefact

### Etape 1 - Charger les 3 artefacts

```powershell
param(
    [Parameter(Mandatory=$true)] [string] $ExtractPath,
    [Parameter(Mandatory=$true)] [string] $ScorePath,
    [Parameter(Mandatory=$true)] [string] $PropagatePath
)

$extract = Get-Content $ExtractPath | ConvertFrom-Yaml
$score = Get-Content $ScorePath | ConvertFrom-Yaml
$propagate = Get-Content $PropagatePath | ConvertFrom-Yaml
```

### Etape 2 - Assembler l'artefact final

```powershell
$artefact = @{
    reposcope_compare = @{
        target_repo = $extract.extraction.source
        analyzed_at = (Get-Date -Format "o")
        extractor_version = "1.0"
        dimensions_extracted = @{
            semantic = @{
                topics = $extract.extraction.semantic.topics
                languages = $extract.extraction.semantic.languages
                readme_summary = $extract.extraction.semantic.readme_summary
            }
            technical = @{
                frameworks = $extract.extraction.technical.frameworks
                architecture_pattern = $extract.extraction.technical.architecture_pattern
                maturity_score = $extract.extraction.technical.maturity_score
            }
            architectural = @{
                strata_coverage = @{} # A enrichir par scoring.macro si necessaire
                inferred_role = $extract.extraction.architectural.inferred_trit_role
            }
        }
        macro_score = @{
            cluster_coverage_gap = $score.scoring.macro.cluster_coverage_gap
            strata_target = $score.scoring.macro.strata_target
            uniqueness_score = $score.scoring.macro.uniqueness_score
        }
        meso_matches = @()
        atomic_matches = @{
            top_5 = @()
            top_20_full = "NEXUS/reposcope/score_$($extract.extraction.source.Replace('/', '_'))_$(Get-Date -Format 'yyyyMMdd').yaml"
        }
        action = ""
        phi_delta_max = 0.0
    }
}
```

### Etape 3 - Peupler les matches MESO

```powershell
foreach ($meso in $score.scoring.meso) {
    $artefact.reposcope_compare.meso_matches += @{
        organ = $meso.organ
        score = $meso.score
        trit_alignment = $meso.trit_alignment
    }
}
```

### Etape 4 - Peupler les matches ATOMIQUE (top 5)

```powershell
$top5 = $score.scoring.atomic.top_20 | Select-Object -First 5
foreach ($atomic in $top5) {
    $artefact.reposcope_compare.atomic_matches.top_5 += @{
        repo = $atomic.repo
        score = $atomic.score
        classification = $atomic.classification
    }
}
```

### Etape 5 - Calculer phi-delta max et recommandation d'action

```powershell
$phiMax = $score.scoring.atomic.top_20 | Select-Object -First 1 -ExpandProperty score
$artefact.reposcope_compare.phi_delta_max = [Math]::Round($phiMax, 3)

if ($phiMax -gt 0.7) {
    $artefact.reposcope_compare.action = "escalate"
} elseif ($phiMax -ge 0.3) {
    $artefact.reposcope_compare.action = "promote"
} else {
    $artefact.reposcope_compare.action = "archive"
}
```

### Etape 6 - Sauvegarder l'artefact NEXUS

```powershell
$slug = $extract.extraction.source.Replace("/", "_")
$dateStr = (Get-Date -Format 'yyyyMMdd')
$outputPath = "NEXUS/reposcope/reposcope_compare_${slug}_${dateStr}.yaml"

$yaml = $artefact | ConvertTo-Yaml -Depth 10
$yaml | Out-File -FilePath $outputPath -Encoding UTF8
Write-Output "[reposcope-artefact] Artefact final ecrit: $outputPath"
Write-Output "[reposcope-artefact] phi-delta max: $phiMax -> Action: $($artefact.reposcope_compare.action)"
```

### Etape 7 - Tracking ARGUS

```powershell
# Charger ou creer l'historique
$historyPath = "ARGUS/reposcope-history.yaml"
$history = @{ comparisons = @() }
if (Test-Path $historyPath) {
    $history = Get-Content $historyPath | ConvertFrom-Yaml
}

# Ajouter l'entree
$history.comparisons += @{
    target_repo = $extract.extraction.source
    analyzed_at = (Get-Date -Format "o")
    phi_delta_max = $phiMax
    top_1_repo = ($score.scoring.atomic.top_20 | Select-Object -First 1 -ExpandProperty repo)
    action = $artefact.reposcope_compare.action
    artifact_path = $outputPath
}

# Sauvegarder l'historique
$history | ConvertTo-Yaml -Depth 5 | Out-File -FilePath $historyPath -Encoding UTF8
Write-Output "[reposcope-artefact] Entree ARGUS ajoutee"
```

### Etape 8 - Detection de drift (optionnel)

```powershell
# Rechercher l'analyse precedente pour ce meme repo
$previous = $history.comparisons | Where-Object { $_.target_repo -eq $extract.extraction.source } | 
            Sort-Object { $_.analyzed_at } -Descending | Select-Object -Skip 1 -First 1

if ($previous) {
    $delta = [Math]::Abs($phiMax - $previous.phi_delta_max)
    if ($delta -gt 0.2) {
        Write-Output "[reposcope-artefact] [WARN] DRIFT DETECTED: Deltaphi-delta = $delta (> 0.2)"
        # Notification FLUX optionnelle pourrait etre ajoutee ici
    }
} else {
    Write-Output "[reposcope-artefact] Premiere analyse pour ce repo"
}
```

## Gestion d'erreurs

| Erreur | Action |
|---|---|
| Artefact manquant | `Write-Output "[ERROR] Fichier manquant: $path"` + exit 1 |
| YAML mal forme | Capturer exception, afficher ligne erreur |
| Repertoire de sortie absent | Creer recursivement avec `New-Item -ItemType Directory -Path (Split-Path $outputPath) -Force` |

## Criteres de succes

- [ ] Artefact YAML valide produit dans NEXUS
- [ ] Recommandation d'action correcte (archive/promote/escalate)
- [ ] ARGUS enregistre chaque comparaison
- [ ] Detection de drift fonctionnelle (Deltaphi-delta > 0.2 -> alerte)
- [ ] Fichiers immuables (pas d'overwrite)

## Skills lies

- **reposcope-extract** : produit l'artefact d'extraction
- **reposcope-score** : produit l'artefact de scoring
- **reposcope-propagate** : produit l'artefact de propagation
- **reposcope-compare** : orchestre le pipeline complet
