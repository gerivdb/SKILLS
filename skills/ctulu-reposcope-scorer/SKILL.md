# Skill: ctulu-reposcope-scorer

## Contexte
Le stage SCORE du pipeline REPOSCOPE-COMPARE. Calcule les scores multicritères pondérés pour chaque repo et génère le classement.

## Outil CTULU
- **Package**: `reposcope_scorer` (PRD-081)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\reposcope-scorer\`
- **CLI**: `reposcope-scorer --data <parquet> --weights <yaml> [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
reposcope-scorer --data data/reposcope_data_20260616.parquet --weights config/scorer_weights.yaml --out scores/ --output json
```

## Pondération par défaut
| Critère | Poids | Description |
|---|---|---|
| `phi_cps` | 0.30 | Score φ-CPS (calculé par scorer) |
| `commits_30d` | 0.20 | Activité récente |
| `has_tests` | 0.15 | Présence de tests |
| `open_issues_ratio` | 0.15 | Ratio inversé (moins = mieux) |
| `deps_count` | 0.10 | Nombre de dépendances |
| `stars` | 0.10 | Popularité |

## Classification
- **Collision** (score ≥ 0.50): doublon potentiel, même strate
- **Synergie** (score ∈ [0.30, 0.50]): complémentarité entre strates
- **Neutre** (score < 0.30): pas d'interaction significative

## Configuration YAML
```yaml
# config/scorer_weights.yaml
phi_cps: 0.30
commits_30d: 0.20
has_tests: 0.15
open_issues_ratio: 0.15
deps_count: 0.10
stars: 0.10
threshold_collision: 0.50
threshold_synergie: 0.30
```

## Sorties
- `scored_<timestamp>.parquet`: DataFrame enrichi avec scores
- `scores_<timestamp>.json`: Top-20 JSON avec classification

## Anti-patterns
- Ne JAMAIS modifier les poids sans recalculer tous les scores
- Ne JAMAIS classifier sans normalisation min-max préalable
- Ne JAMAIS utiliser un seuil collision < 0.30 (faux positifs)
