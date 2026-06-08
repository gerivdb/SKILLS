---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xARGUS_PIPELINE_RUNNER_20260608
status: active
---

# Skill: argus-pipeline-runner

## Purpose
Orchestrate the full ARGUS pipeline: TINA ingest → SGR gap detection → ARGUS scanners → Archive.

## Context
The pipeline runs daily at 06h00 via KIVA-CLI cron. It can also be triggered manually. Each step depends on the previous one's output.

## Pipeline steps

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

## Manual run

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

## Validation

After full pipeline run:
- SGR: 0 P1/P2/P3 gaps (or only documented exceptions)
- ARGUS: combined score = 1.00
- Archive: all reports in NEXUS/reports/

## Anti-patterns

- **DON'T** run SGR before TINA ingest completes
- **DON'T** skip scanner validation after pipeline run
- **DON'T** modify reports manually — always re-run the pipeline
