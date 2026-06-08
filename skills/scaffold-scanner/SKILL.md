---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xSCAFFOLD_SCANNER_20260608
status: active
---

# Skill: scaffold-scanner

## Purpose
Generate a declarative scanner YAML from an SGR gap report — bridge between gap detection and scanner creation.

## Context
When SGR detects a gap (P1/P2/P3), the `scaffold-scanner` protocol creates a scanner YAML that will close that gap. The output is ready to use with `declarative-scanner-builder`.

## Protocol

### Step 1 — Identify the gap

From GAP_REPORT, extract:
- `gap_id`: e.g., `REPO_UNCOVERED_CANDIDATOR`
- `severity`: P1/P2/P3
- `source`: repo or citizen name
- `trit`: triggering primitive
- `action`: remediation text

### Step 2 — Determine CHECK_TYPE from gap pattern

| Gap pattern | CHECK_TYPE | Params |
|-------------|------------|--------|
| `REPO_UNCOVERED_*` (scanner missing) | `composite` (OR) | Sub-checks per strate |
| `SKILL_ORPHAN_*` (no trit_primitive) | `command` | Count orphans in skills dir |
| `TRIT_ORPHAN_*` (no implementation) | `yaml_query` | Query SymbolGraph edges |
| `CITIZEN_UNBACKED_*` (no ADR) | `yaml_query` | Query citizens.yaml |
| `*_STALE_*` (old file) | `file_age` | glob + max_age_hours |
| `*_MISSING_*` (file absent) | `file_exists` | path |

### Step 3 — Generate scanner YAML

Use the template from `declarative-scanner-builder` skill. Fill:
- `scanner_id`: `{slug}_health` (from source name)
- `citizen`: source name from gap
- `trit`: from gap's trit field
- `checks`: 1 primary check per gap pattern

### Step 4 — Customize CHECK_TYPE params

For `REPO_UNCOVERED_*` gaps, the primary check should verify:
- STRATUM_RELAY.md exists (COV-001)
- ECOS_ROOT.json exists (COV-003)
- README.md exists (COV-004)

For `SKILL_ORPHAN_*` gaps, use `command` type with Python orphan counter.

### Step 5 — Test and iterate

Run scanner → check score → adjust CHECK_TYPE params if needed.

## CLI Command

```powershell
# Single gap
python -m kiva scaffold scanner --gap-id SGR-TEST-001 `
  --from-report GAP_REPORT.yaml `
  --output-dir ARGUS/scanners/declared/

# All P1 gaps
python -m kiva scaffold scanner --all-p1 `
  --from-report GAP_REPORT.yaml
```

## Anti-patterns

- **DON'T** scaffold without first checking if a scanner already exists
- **DON'T** use `command` type for simple file checks — prefer built-in types
- **DON'T** forget to run the scanner after scaffolding to validate
