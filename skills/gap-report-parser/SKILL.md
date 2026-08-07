---
type: skill
version: "2.0.0"
date: "2026-06-08"
intent_hash: 0xGAP_REPORT_PARSER_V2_20260608
status: active
---

# Skill: gap-report-parser

## Purpose
Parse SGR GAP_REPORT and manage the complete gap lifecycle - detection, triage, resolution, verification, and closure.

## Context
SGR produces `GAP_REPORT_{timestamp}.json` with `by_priority` sections (P1/P2/P3). Each gap has: `id`, `title`, `severity`, `source`, `trit`, `action`, `status`. This skill covers both parsing AND lifecycle management.

## Parsing protocol

### Step 1 - Locate latest report

```powershell
$report = Get-ChildItem "D:\DO\WEB\TOOLS\L0-CANON\NEXUS\citizens\SystemicGapReasoner\reports\GAP_REPORT_*.json" |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Step 2 - Parse with Python

```python
import json, yaml
from pathlib import Path

report = json.loads(Path("GAP_REPORT.json").read_text())

# Count by priority
for prio in ["P1", "P2", "P3"]:
    gaps = report.get("by_priority", {}).get(prio, [])
    print("{}: {} gaps".format(prio, len(gaps)))

# Extract specific gap types
repo_gaps = [g for g in report.get("by_priority", {}).get("P2", [])
             if g.get("id", "").startswith("REPO_UNCOVERED_")]
skill_gaps = [g for g in report.get("by_priority", {}).get("P3", [])
              if g.get("id", "").startswith("SKILL_ORPHAN_")]
```

### Step 3 - Determine action per gap type

| Gap prefix | Action | Skill to use |
|------------|--------|--------------|
| `REPO_UNCOVERED_*` | Create STRATUM_RELAY.md + ECOS_ROOT.json | `repo-coverage-batch` |
| `SKILL_ORPHAN_*` | Patch trit_primitive | `skill-trit-patcher` |
| `TRIT_ORPHAN_*` | Link primitive to workflow/citizen | manual |
| `CITIZEN_UNBACKED_*` | Create ADR backing | manual |

### Step 4 - Check exceptions

Before acting, check if gap_id is in `sgr.yaml` exceptions list:

```python
exceptions = yaml.safe_load(open("config/sgr.yaml"))["exceptions"]
excepted_ids = {e["gap_id"] for e in exceptions}
```

## Gap lifecycle management

### Phase 1 - Detection
SGR run produces GAP_REPORT. Parse and count.

### Phase 2 - Triage
For each gap: determine type -> assign action -> check exceptions.

### Phase 3 - Resolution
- **Scanner creation**: Use `scaffold-scanner` -> test -> register in argus.yaml
- **Batch patch**: Use `patch_skill_frontmatter.py` -> verify with scanner
- **Exception**: Document in sgr.yaml with reason + review date

### Phase 4 - Verification
Re-run SGR. Compare with previous report. All targeted gaps should be gone.

### Phase 5 - Closure
Archive report to NEXUS/reports/sgr/. Update session summary.

## Exception format

```yaml
- gap_id: "REPO_UNCOVERED_NEXUS"
  reason: "NEXUS est le SOT data - couverture deleguee"
  approved_by: "HITL-2026-06-08"
  review_date: "2026-09-08"
```

## Anti-patterns

- **DON'T** act on gaps without checking exceptions first
- **DON'T** parse without validating report structure
- **DON'T** forget to re-run SGR after fixes
- **DON'T** leave scanners unregistered in argus.yaml
