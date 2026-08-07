---
name: reposcope-propagate
version: "1.0"
intent_hash: 0xSKILL_REPOSCOPE_PROPAGATE_20260615
---

# Skill: reposcope-propagate

## Quand l'utiliser

- Un artefact de scoring YAML (produit par `reposcope-score`) est disponible
- Le pipeline REPOSCOPE-COMPARE necessite la propagation vers les organes concernes
- ECOS-CLI `reposcope-propagate --input <score.yaml>` est appele

**NE PAS utiliser** sans un artefact de scoring valide en entree.

## References

- **INTENT** : INTENT-041c (GOVERNANCE-HUB)
- **PRD** : PRD-REPOSCOPE-PROPAGATION-2026-06-15
- **EPIC** : EPIC-REPOSCOPE-PROPAGATION

## Pipeline de propagation

### Etape 1 - Charger le scoring

```powershell
$score = Get-Content $InputPath | ConvertFrom-Yaml
$source = $score.scoring.source
$top20 = $score.scoring.atomic.top_20
```

### Etape 2 - Filtrer par seuils

```powershell
$thresholdResonant = 0.30
$thresholdStrong = 0.50

$resonant = $top20 | Where-Object { $_.score -ge $thresholdResonant }
$strong = $top20 | Where-Object { $_.score -ge $thresholdStrong }
$collisions = $top20 | Where-Object { $_.classification -eq "collision" }
$synergies = $top20 | Where-Object { $_.classification -eq "synergie" }
```

### Etape 3 - Generer evenements FLUX

```powershell
$fluxEvents = @()
foreach ($repo in $resonant) {
    $fluxEvents += @{
        flux_event = @{
            type = "reposcope_comparison_result"
            source = $source
            target = $repo.repo
            score = $repo.score
            classification = $repo.classification
            timestamp = (Get-Date -Format "o")
        }
    }
}

# Ecrire les evenements
$slug = $source.Replace("/", "_")
$fluxPath = "FLUX/events/reposcope_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
$fluxEvents | ConvertTo-Yaml -Depth 5 | Out-File -FilePath $fluxPath -Encoding UTF8
```

### Etape 4 - Notifier BRAIN-FEED

```powershell
$brainFeed = @"
# REPOSCOPE-COMPARE - Resultat de comparaison

**Source**: $source
**Date**: $(Get-Date -Format "yyyy-MM-dd HH:mm")

## Top 5 repos resonants

| Rang | Repo | Score | Classification |
|------|------|-------|----------------|
"@
for ($i = 0; $i [Math]::Min(5, $resonant.Count); $i++) {
    $r = $resonant[$i]
    $brainFeed += "`n| $($i+1) | $($r.repo) | $($r.score) | $($r.classification) |"
}

$brainFeed += @"

## Resume
- **Repos resonants** (>= 0.30): $($resonant.Count)
- **Fortement resonants** (>= 0.50): $($strong.Count)
- **Collisions detectees**: $($collisions.Count)
- **Synergies detectees**: $($synergies.Count)

## Recommandation
"@
$phiMax = ($top20 | Select-Object -First 1).score
if ($phiMax -gt 0.7) {
    $brainFeed += "`n[WARN] **ESCALATE** - Collision forte detectee (phi-delta max: $phiMax). Decision humaine requise."
} elseif ($phiMax -ge 0.3) {
    $brainFeed += "`n[CLIPBOARD] **PROMOTE** - Correspondance moderee (phi-delta max: $phiMax). Etude humaine recommandee."
} else {
    $brainFeed += "`n[OK] **ARCHIVE** - Pas de correspondance significative (phi-delta max: $phiMax)."
}

$brainFeedPath = "BRAIN/brain-feed/inbox/reposcope-compare-${slug}-$(Get-Date -Format 'yyyyMMdd').md"
$brainFeed | Out-File -FilePath $brainFeedPath -Encoding UTF8
```

### Etape 5 - Note Gitnote

```powershell
$gitnote = @"
---
type: NOTE
status: draft
date: "$(Get-Date -Format 'yyyy-MM-dd')"
intent_hash: 0xREPOSCOPE_COMPARE_${slug}_$(Get-Date -Format 'yyyyMMdd')
---

# REPOSCOPE-COMPARE: $source

## Metadonnees
- **Source**: $source
- **Date**: $(Get-Date -Format "o")
- **phi-delta max**: $phiMax
- **Action**: $(if ($phiMax -gt 0.7) { "escalate" } elseif ($phiMax -ge 0.3) { "promote" } else { "archive" })

## Top 10 repos resonants

| Repo | Score | Classification |
|------|-------|----------------|
"@
$top20 | Select-Object -First 10 | ForEach-Object {
    $gitnote += "`n| $($_.repo) | $($_.score) | $($_.classification) |"
}

$gitnote += @"

## Artefacts
- **Extraction**: NEXUS/reposcope/extract_${slug}_*.yaml
- **Scoring**: NEXUS/reposcope/score_${slug}_*.yaml
- **Evenements FLUX**: FLUX/events/reposcope_${slug}_*.yaml
"@

$gitnotePath = "Gitnote/ideas/inbox/reposcope-compare-${slug}-$(Get-Date -Format 'yyyyMMdd').md"
$gitnote | Out-File -FilePath $gitnotePath -Encoding UTF8
```

### Etape 6 - Sortie YAML

```powershell
$propagation = @{
    propagation = @{
        source = $source
        propagated_at = (Get-Date -Format "o")
        version = "1.0"
        thresholds = @{ resonant = $thresholdResonant; strongly_resonant = $thresholdStrong }
        resonant_repos_count = $resonant.Count
        strongly_resonant_count = $strong.Count
        events_emitted = $fluxEvents.Count
        collisions_detected = $collisions.Count
        synergies_detected = $synergies.Count
    }
}

$slug = $source.Replace("/", "_")
$outputPath = "NEXUS/reposcope/propagate_${slug}_$(Get-Date -Format 'yyyyMMdd').yaml"
$propagation | ConvertTo-Yaml -Depth 5 | Out-File -FilePath $outputPath -Encoding UTF8
Write-Output "[reposcope-propagate] Artefact ecrit: $outputPath"
Write-Output "[reposcope-propagate] $($resonant.Count) repos resonants, $($collisions.Count) collisions, $($synergies.Count) synergies"
```

## Criteres de succes

- [ ] Repos >= 0.30 classes "resonant"
- [ ] Repos >= 0.50 classes "fortement resonant"
- [ ] Evenements FLUX emis pour chaque repo resonant
- [ ] BRAIN-FEED notifie avec resume markdown
- [ ] Note Gitnote creee dans ideas/inbox/

## Skills lies

- **reposcope-score** : produit l'artefact de scoring en entree
- **reposcope-artefact** : assemble l'artefact final NEXUS
- **reposcope-compare** : orchestre le pipeline complet
