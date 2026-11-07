---
name: recall-ouroboros
description: Recherche récursive sur la mémoire KiloCode locale pour dépasser la limite de 12 termes par requête de `kilo_local_recall`. Décompose une requête large en passes atomiques, agrège, déduplique et converge vers une carte complète des sessions pertinentes. Utiliser quand la recherche couvre plusieurs sujets transverses ou quand une seule requête `kilo_local_recall` est insuffisante.
---

# Recall Ouroboros

## Objectif
Dépasser la limite de **12 termes par requête** de `kilo_local_recall` par une exécution en passes contrôlées et un cycle d’enrichissement itératif.

## Déclencheur
- Requête large (> 12 termes) sur la mémoire KiloCode
- Sujet transverse couvrant plusieurs worktrees / sessions
- Besoin de carte exhaustive avant décision architecturale

## Entrées
| Param | Type | Requis | Défaut |
|-------|------|--------|--------|
| `query` | string | ✅ | — |
| `max_passes` | int | ❌ | `5` |
| `convergence_threshold` | float | ❌ | `0.2` |
| `parallel` | bool | ❌ | `false` |
| `limit` | int | ❌ | `20` |

## Sortie
JSON conforme au contrat :
```json
{
  "tool": "recall-ouroboros",
  "query": "string",
  "passes": 3,
  "converged": true,
  "sessions": [...],
  "extracted_terms": [...],
  "coverage": {...}
}
```

## Bridges — Phase 1 (structures formelles)

Recall Ouroboros alimente les **architectures centrales** de l'écosystème via 4 bridges :

| Bridge | Cible | Entrée | Sortie |
|--------|-------|--------|--------|
| `admg_ml` | ADMG-ML | `sessions[]`, `extracted_terms[]`, `pass_log[]` | Manifest ADMG-ML (`wf`, `slice`, `validate`) |
| `kg_l` | KG-L | `sessions[]`, `extracted_terms[]`, co-occurrences | Graphe KG-L (`nodes`, `edges` avec EdgeKind) |
| `talex` | TALEX | `sessions[]`, `extracted_terms[]`, `pass_log[]` | Payload UnifiedSemanticGraph |
| `holmes` | HOLMES | `sessions[]`, `extracted_terms[]`, edges KG-L | Narrative causale (`acts`: problem/suspects/motives/resolution) |

### Étape 4 bis — Bridges
```powershell
# Exécuter Recall Ouroboros + toutes les bridges
python .kilo/skills/recall-ouroboros/recall-ouroboros.py --mode bridges --query "<requête>"

# Exécuter une bridge spécifique
python -c "import sys; sys.path.insert(0, '.kilo/skills/recall-ouroboros'); from bridges.kg_l_bridge import build_kg_l_graph; import json; print(json.dumps(build_kg_l_graph(<result>), indent=2))"
```

## Workflow

### Étape 1 — Vérification préalable
```powershell
# Agent budget check (ADMG-ML/KG-L écosystème = atomique mais mémoire locale)
pwsh .kilo/scripts/session-start-checklist.ps1
```

### Étape 2 — Décomposition
```powershell
python .kilo/skills/recall-ouroboros/recall-ouroboros.py --mode decompose --query "<requête large>"
```

### Étape 3 — Exécution des passes
```powershell
# Séquentiel (défaut)
python .kilo/skills/recall-ouroboros/recall-ouroboros.py --mode run --query "<requête>"

# Parallèle (si RAM > 16 Go)
python .kilo/skills/recall-ouroboros/recall-ouroboros.py --mode run --query "<requête>" --parallel
```

### Étape 4 — Synthèse
```powershell
python .kilo/skills/recall-ouroboros/recall-ouroboros.py --mode synthesize --output recall-ouroboros-result.json
```

## Règles
- Max 12 termes par sous-requête
- Max 5 passes par exécution
- Arrêt si convergence < 20% nouveaux termes
- Déduplication stricte par `session_id`
- Pas de modification de `kilo_local_recall`

## Références
- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-RECALL-OUROBOROS-2026-08-12.md`
- IntentHash : `0xPRD_MOC_RECALL_OUROBOROS_20260812`
