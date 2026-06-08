---
name: kiva-pipeline
description: "KIVA-CLI pipeline cron 06h00, TINA→SGR→ARGUS, scaffold scanner CLI, declarative engine. Use when user mentions 'KIVA pipeline', 'cron', 'scaffold scanner', 'declarative_runner'."
version: "2.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale — diagnostic matériel Z600"}
  - {v: "2.0.0", date: "2026-06-08", notes: "Refonte — pipeline cron, scaffold CLI, moteur déclaratif"}
triggers: ["KIVA pipeline", "cron 06h00", "scaffold scanner", "declarative_runner"]
layer: "L3_CITIZEN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritIsolate
---
# KIVA Pipeline v2

## Domaine et périmètre

KIVA-CLI orchestre le pipeline quotidien TINA→SGR→ARGUS. v2 = cron 06h00 + scaffold scanner CLI + moteur déclaratif YAML.

## Architecture v2

```
Cron 06h00 (KIVA-CLI pipelines/tina-sgr-daily.yaml)
  │
  ├─ Step 1: TINA --ingest-all (73 primitives, 209 nodes)
  ├─ Step 2: SGR v2 --full (gap detection → 6 exceptions)
  ├─ Step 3: ARGUS 5 scanners (score 1.00)
  └─ Step 4: Archive → NEXUS/reports/
```

## Scaffold Scanner CLI

```powershell
# Créer un scanner depuis un gap SGR
python -m kiva scaffold scanner --gap-id SGR-TEST-001 `
  --from-report GAP_REPORT.yaml `
  --output-dir ARGUS/scanners/declared/

# Batch : tous les P1 ouverts
python -m kiva scaffold scanner --all-p1 `
  --from-report GAP_REPORT.yaml
```

## Pipeline YAML

Fichier : `KIVA-CLI/pipelines/tina-sgr-daily.yaml`

Étapes :
1. `tina_ingest` — python -m symbol_graph --ingest-all
2. `sgr_run` — python -m sgr --full
3. `check-p1-gaps` — Gate 0 P1 tolérés
4. `push-report` — Archive NEXUS/reports/

## Moteur déclaratif

- 8 CHECK_TYPES : file_exists, file_age, yaml_query, yaml_contains, key_present, command, composite
- Fichiers YAML dans `ARGUS/scanners/declared/`
- Test : `python -m engine.declarative_runner {scanner}.yaml`

## CHECK_INFERENCE_RULES

When creating scanners from gaps, the scaffold_scanner infers CHECK_TYPE from gap pattern:

| Gap pattern | Inferred CHECK_TYPE | Params |
|-------------|---------------------|--------|
| `REPO_UNCOVERED_*` | `composite` (OR) | Sub-checks: STRATUM_RELAY, ECOS_ROOT, README |
| `SKILL_ORPHAN_*` | `command` | Count orphans via Python |
| `TRIT_ORPHAN_*` | `yaml_query` | Query SymbolGraph edges |
| `CITIZEN_UNBACKED_*` | `yaml_query` | Query citizens.yaml |
| `*_STALE_*` | `file_age` | glob + max_age_hours |
| `*_MISSING_*` | `file_exists` | path |

## Scaffold Scanner (scaffold_scanner)

The `scaffold_scanner` CLI command creates a declarative scanner YAML from a SGR gap:

```powershell
# Single gap → single scanner
python -m kiva scaffold scanner --gap-id SGR-TEST-001 `
  --from-report GAP_REPORT.yaml `
  --output-dir ARGUS/scanners/declared/

# Batch: all P1 gaps → multiple scanners
python -m kiva scaffold scanner --all-p1 `
  --from-report GAP_REPORT.yaml

# With custom template
python -m kiva scaffold scanner --gap-id SGR-TEST-001 `
  --from-report GAP_REPORT.yaml `
  --template composite_or `
  --register  # auto-register in argus.yaml
```

Output: `ARGUS/scanners/declared/{slug}_health.yaml` ready for `declarative_runner`.

## Référence

- Pipeline : `KIVA-CLI/pipelines/tina-sgr-daily.yaml`
- Scaffold CLI : `KIVA-CLI/kiva_cli/commands/scaffold_scanner.py`
- Moteur : `ARGUS/engine/declarative_runner.py`
- Skills : `L4-TOOLS/SKILLS/skills/scaffold-scanner/SKILL.md`
- P15 flat reference : `L4-TOOLS/SKILLS/perplexity/skills/scaffold-scanner.md`
