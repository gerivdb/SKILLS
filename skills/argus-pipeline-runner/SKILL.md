---
type: skill
version: "1.1.0"
date: "2026-06-28"
intent_hash: 0xARGUS_PIPELINE_RUNNER_20260628
status: active
---

# Skill: argus-pipeline-runner

## Purpose
Orchestrate the full ARGUS pipeline: Impense detection → Qualification → Orientation → Closure.

## Context
ARGUS est la couche de surveillance des interstices du metacluster gerivdb. Le pipeline
detecte les impenses (gaps entre objets de gouvernance), les qualifie, oriente vers un
artefact de resolution, et trace la fermeture dans `gap_registry.yaml`.

Ce skill couvre deux pipelines:
1. **Legacy pipeline** (v1.0): TINA → SGR → ARGUS scanners → Archive
2. **Impense pipeline** (v1.1): detect → qualifier → orienter → fermer

## ARGUS Impense Pipeline (v1.1 — 2026-06-28)

### Detect → Qualify → Orienter → Fermer

Reference: ADR-2026-06-27-001-ARGUS-INTERSTICES (NEXUS/ADR/)

```
[1] DETECT
    Scanner les interstices entre clusters
    Tools: gap_detector.py (CTULU), conftest.py ENV2
        |
        v
[2] QUALIFIER
    Typer le gap (coverage/liaison/coherence/anticipation)
    Schema: ONTOLOGY/schema/gap_registry.schema.yaml
    Tools: schema validation (Pydantic/jsonschema)
        |
        v
[3] ORIENTER
    Determiner l'artefact cible de resolution:
    -> Gap coverage   : creer Intent ou ADR
    -> Gap liaison      : ajouter lien formel (reference croisee)
    -> Gap coherence    : ouvrir ADR de reconciliation
    -> Gap anticipation : elever en EPIC ou roadmap item
    Tools: CTULU graph_builder + ADR pattern router
        |
        v
[4] FERMER
    Creer l'artefact de resolution
    Conserver trace dans NEXUS/ARGUS/gap_registry.yaml
    Marquer le gap CLOSED avec reference a l'artefact cree
```

### gap_registry.yaml format

Canonical schema: `https://github.com/gerivdb/ONTOLOGY/blob/main/schema/gap_registry.schema.yaml`

```yaml
version: "1.0.0"
generated_at: "YYYY-MM-DD HH:MM:SS+02:00"
scope: "gerivdb/*"

gaps:
  - id: "GAP-YYYY-MM-DD-NNN"
    type: coverage | liaison | coherence | anticipation
    status: detected | qualified | oriented | closed
    criticality: low | medium | high | critical
    title: "..."
    description: > ...
    detected_at: "YYYY-MM-DD"
    detected_by: "ENV-session"
    source_objects:
      - repo: "gerivdb/<REPO>"
        path: "<file>"
        type: intent | adr | epic | roadmap | encours | repo | other
    target_artefact:
      artefact_type: intent | adr | epic | roadmap | crossref | encours
      action: "<action>"
      repo: "gerivdb/<REPO>"
    resolution:
      repo: "gerivdb/<REPO>"
      path: "<file>"
      closed_at: "YYYY-MM-DD"
    tags: [CONFORME_NEXUS]
```

### Current registry

`NEXUS/ARGUS/gap_registry.yaml` — 3 gaps tous `closed` (GAP-001, GAP-002, GAP-003):
- GAP-001: INTENT-069 sans definition canonique dans ONTOLOGY → resolu par concepts/impense.md
- GAP-002: ADR ARGUS-INTERSTICES sans schema gap_registry → resolu par schema/gap_registry.schema.yaml
- GAP-003: CTULU PR#81 mergee sans tests → resolu par 35/35 tests governance verifs (2026-06-28)

---

## Legacy Pipeline (v1.0 — TINA/SGR/ARGUS scanners)

### Pipeline steps

```
Step 1: TINA --ingest-all
  Input:  TritRegistry.yaml + known_repositories.yaml + skills dir
  Output: symbolgraph-{date}.json (209 nodes, 79 edges)

Step 2: SGR v2 --full
  Input:  symbolgraph-latest.json + config/sgr.yaml
  Output: GAP_REPORT_{timestamp}.json (gaps by priority)

Step 3: ARGUS scanners (3 scanners)
  Input:  GAP_REPORT + repo files + configs
  Output: ARGUS_REPORT_{timestamp}.json (score per scanner)

Step 4: Archive
  Input:  All reports
  Output: NEXUS/reports/sgr/ + NEXUS/reports/tina/ + NEXUS/reports/argus/
```

### Manual run

```powershell
# Full pipeline
cd D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
python -m kiva run pipelines/tina-sgr-daily.yaml

# Or step by step:
# Step 1
cd D:\DO\WEB\TOOLS\L3-CITIZENS\TINA
python -m symbol_graph --ingest-all `
  --trit-registry D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\TritRegistry.yaml `
  --extra-registries D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\TritRegistry-political-compass.yaml `
  --known-repos D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\known_repositories.yaml `
  --skills D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills\ `
  --output D:\DO\WEB\TOOLS\reports\tina\symbolgraph-latest.json

# Step 2
cd D:\DO\WEB\TOOLS\L0-CANON\NEXUS\citizens\SystemicGapReasoner
python run_sgr.py

# Step 3
cd D:\DO\WEB\TOOLS\L3-CITIZENS\ARGUS
$env:PYTHONPATH = "."
python -m engine.declarative_runner scanners/declared/mc_rnn_health.yaml
python -m engine.declarative_runner scanners/declared/kiva_pipeline_health.yaml `
  kiva_root=D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI `
  reports_root=D:\DO\WEB\TOOLS\reports
python -m engine.declarative_runner scanners/declared/gateway_manager_health.yaml `
  gm_root=D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER
python -m engine.declarative_runner scanners/declared/repo_coverage_health.yaml `
  repo_name=KIVA-CLI repo_root=D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI `
  gov_root=D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
python -m engine.declarative_runner scanners/declared/skill_trit_coverage.yaml `
  skills_dir=D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills `
  gov_root=D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
```

### Validation

After full pipeline run:
- SGR: 0 P1/P2/P3 gaps (or only documented exceptions)
- ARGUS: combined score = 1.00
- Archive: all reports in NEXUS/reports/

## Anti-patterns

- **DON'T** run SGR before TINA ingest completes
- **DON'T** skip scanner validation after pipeline run
- **DON'T** modify reports manually — always re-run the pipeline
- **DON'T** leave gaps in `oriented` status without resolution target
- **DON'T** create gaps without validating against `gap_registry.schema.yaml`
