---
name: argus-tracker
description: "ARGUS scanners déclaratifs, moteur YAML 8 CHECK_TYPES, pipeline TINA→SGR→ARGUS. Use when user mentions 'ARGUS scanner', 'declarative_runner', 'CHECK_TYPES', 'skill_trit_coverage', 'repo_coverage_health'."
version: "2.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale — phases/deltas"}
  - {v: "2.0.0", date: "2026-06-08", notes: "Refonte — scanners déclaratifs YAML, moteur 8 CHECK_TYPES"}
triggers: ["ARGUS scanner", "declarative_runner", "CHECK_TYPES", "skill_trit_coverage"]
layer: "L3_CITIZEN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritObserve
---
# ARGUS Tracker v2

## Domaine et périmètre

ARGUS est le moteur de surveillance de l'écosystème gerivdb. v2 = scanners déclaratifs YAML (8 CHECK_TYPES) + pipeline TINA→SGR→ARGUS.

## Architecture v2

```
TINA SymbolGraph (209 nodes, 73 primitives)
  → SGR v2 (gap detection, scanner générique)
    → ARGUS 3+ scanners (score combiné 1.00)
      → KIVA-CLI pipeline (cron 06h00)
        → Archive NEXUS/reports/
```

## CHECK_TYPES disponibles

| Type | Purpose | Params |
|------|---------|--------|
| `file_exists` | Vérifier existence fichier | `path` |
| `file_age` | Vérifier fraîcheur fichier | `glob`, `max_age_hours` |
| `yaml_query` | Requêter contenu YAML | `file`, `query`, `expect_empty` |
| `yaml_contains` | Vérifier valeurs YAML | `file`, `keys_path`, `expect_values` |
| `key_present` | Vérifier clé YAML | `file`, `key`, `min_value` |
| `command` | Exécuter commande shell | `cmd`, `expect_returncode` |
| `composite` | Combiner checks (AND/OR) | `operator`, `checks` |

## Scanners actifs (v2)

| Scanner | Fichier | Score |
|---------|---------|-------|
| `mc_rnn_health` | scanners/mc_rnn_health.py | 1.0 |
| `kiva_pipeline_health` | scanners/declared/kiva_pipeline_health.yaml | 1.0 |
| `gateway_manager_health` | scanners/declared/gateway_manager_health.yaml | 1.0 |
| `repo_coverage_health` | scanners/declared/repo_coverage_health.yaml | 1.0 |
| `skill_trit_coverage` | scanners/declared/skill_trit_coverage.yaml | 1.0 |

## Méthodologie

### Créer un nouveau scanner (YAML)

1. Créer `ARGUS/scanners/declared/{scanner_id}.yaml`
2. Utiliser un CHECK_TYPE existant
3. Tester : `python -m engine.declarative_runner {scanner}.yaml`
4. Enregistrer dans `config/argus.yaml`

### Pipeline cron 06h00

```powershell
# KIVA-CLI exécute automatiquement :
# 1. TINA --ingest-all → symbolgraph-latest.json
# 2. SGR v2 --full → GAP_REPORT_{timestamp}.json
# 3. ARGUS 5 scanners → score combiné
# 4. Archive → NEXUS/reports/
```

## Référence

- Moteur : `ARGUS/engine/declarative_runner.py`
- Config : `ARGUS/config/argus.yaml`
- Declarative scanners : `ARGUS/scanners/declared/`
