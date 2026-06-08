---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xDECLARATIVE_SCANNER_BUILDER_20260608
status: active
adr_ref: adr-tina-001-symbolgraph-mc-rnn
trit_primitive: TritIsolate
tags: [argus, scanner, yaml, declarative]
---

# declarative-scanner-builder

## Purpose
Create an ARGUS scanner from a YAML declarative file — no Python coding required.

## Trigger
Use when: creating a new ARGUS scanner, converting a gap to a scanner, or when user mentions "declarative scanner", "scanner YAML".

## Steps

### Step 1 — Define the scanner

```yaml
scanner_id: my_scanner_health
citizen: MY-REPO
trit: TritObserve
version: "1.0.0"

checks:
  - id: MY-001
    severity: P2
    title: "Description of what this checks"
    type: file_exists
    path: "{root}/some_file.yaml"
    remediation: "How to fix if failing"
```

### Step 2 — Place in correct directory

```
ARGUS/scanners/declared/{scanner_id}.yaml
```

### Step 3 — Register in argus.yaml

```yaml
scanners:
  my_scanner:
    path: scanners/declared/my_scanner_health.yaml
    type: declarative
```

### Step 4 — Test

```powershell
python -m engine.declarative_runner scanners/declared/my_scanner_health.yaml `
  root=D:\DO\WEB\TOOLS\L3-CITIZENS\MY-REPO `
  gov_root=D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
```

Expected: `{"healthy": true, "score": 1.0}`

### Step 5 — Verify in SGR

After adding to `argus.yaml`, run SGR to confirm the gap is closed:
```powershell
cd NEXUS/citizens/SystemicGapReasoner
python run_sgr.py
```

## CHECK_TYPES available

| Type | Purpose | Key params |
|------|---------|------------|
| `file_exists` | Verify a file exists | `path` |
| `file_age` | Check file is fresh | `glob`, `max_age_hours` |
| `yaml_query` | Query YAML content | `file`, `query`, `expect_empty` |
| `yaml_contains` | Check YAML has values | `file`, `keys_path`, `expect_values` |
| `key_present` | Check key exists in YAML | `file`, `key`, `min_value` |
| `command` | Run shell command | `cmd`, `expect_returncode` |
| `composite` | Combine checks (AND/OR) | `operator`, `checks` |

## Rules
- Use YAML declarative scanners by default — only write Python when YAML doesn't suffice
- Always use `{root}`, `{gov_root}`, `{reports_root}` placeholders — never hardcode paths
- Always register in `argus.yaml` after creating a scanner YAML
- Prefer built-in CHECK_TYPES over `command` type

## Anti-patterns
- Don't create a Python scanner when YAML suffices
- Don't hardcode paths — use placeholders
- Don't forget to register in `argus.yaml`
- Don't use `command` type when a built-in CHECK_TYPE exists

## Examples

- `ARGUS/scanners/declared/repo_coverage_health.yaml` — parametric, covers all repos
- `ARGUS/scanners/declared/skill_trit_coverage.yaml` — command-based validation
- `ARGUS/scanners/declared/kiva_pipeline_health.yaml` — composite checks
