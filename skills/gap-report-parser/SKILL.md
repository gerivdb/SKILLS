---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xGAP_REPORT_PARSER_20260608
status: active
---

# Skill: gap-report-parser

## Purpose
Parse an SGR GAP_REPORT YAML/JSON to extract gap metadata for scanner scaffolding or triage.

## Context
SGR produces `GAP_REPORT_{timestamp}.json` with `by_priority` sections (P1/P2/P3). Each gap has: `id`, `title`, `severity`, `source`, `trit`, `action`, `status`. This skill extracts structured data for decision-making.

## Protocol

### Step 1 — Locate latest report

```powershell
$report = Get-ChildItem "D:\DO\WEB\TOOLS\L0-CANON\NEXUS\citizens\SystemicGapReasoner\reports\GAP_REPORT_*.json" |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Step 2 — Parse with Python

```python
import json, yaml
from pathlib import Path

report = json.loads(Path("GAP_REPORT.json").read_text())

# Count by priority
for prio in ["P1", "P2", "P3"]:
    gaps = report.get("by_priority", {}).get(prio, [])
    print(f"{prio}: {len(gaps)} gaps")

# Extract specific gap types
repo_gaps = [g for g in report.get("by_priority", {}).get("P2", [])
             if g.get("id", "").startswith("REPO_UNCOVERED_")]
skill_gaps = [g for g in report.get("by_priority", {}).get("P3", [])
              if g.get("id", "").startswith("SKILL_ORPHAN_")]
```

### Step 3 — Determine action per gap type

| Gap prefix | Action |
|------------|--------|
| `REPO_UNCOVERED_*` | Create STRATUM_RELAY.md + ECOS_ROOT.json (see `repo-coverage-batch`) |
| `SKILL_ORPHAN_*` | Patch trit_primitive (see `skill-trit-patcher`) |
| `TRIT_ORPHAN_*` | Link primitive to workflow/citizen |
| `CITIZEN_UNBACKED_*` | Create ADR backing |

### Step 4 — Check exceptions

Before acting, check if gap_id is in `sgr.yaml` exceptions list. If yes, skip.

```python
exceptions = yaml.safe_load(open("config/sgr.yaml"))["exceptions"]
excepted_ids = {e["gap_id"] for e in exceptions}
```

## Anti-patterns

- **DON'T** act on gaps without checking exceptions first
- **DON'T** parse without validating report structure (check `by_priority` key exists)
- **DON'T** forget to re-run SGR after fixes to validate
