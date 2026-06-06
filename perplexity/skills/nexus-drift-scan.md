# NEXUS Drift Scan Skill

## Purpose
Scan NEXUS/managers/ for unauthorized Python files and detect governance drift.

## When to Use
- After any file operation in NEXUS/
- Before committing changes to NEXUS/
- Periodic compliance check (recommended: every 12h)

## Workflow

### Step 1: Run drift scan
```bash
cd D:\DO\WEB\TOOLS\L0-CANON\NEXUS
python -c "from audit.daemon_drift_watcher import DriftWatcher; w = DriftWatcher(); import json; print(json.dumps(w.run_once(), indent=2))"
```

### Step 2: Interpret results
- `drift_detected: false` -- Clean, no action needed
- `drift_detected: true` -- New files found, review required
- `over_threshold: true` -- More than 10 .py files in managers/

### Step 3: If drift detected
1. Review `new_files` list
2. Determine if files belong in NEXUS or should be migrated
3. If migration needed: move to correct repo (WAZAA/src/, AGENT-REGISTRY/src/, etc.)
4. Update `NEXUS/.audit/drift_watcher_state.json` baseline

### Step 4: Check phi-CPS compliance
```bash
cd D:\DO\WEB\TOOLS\L0-CANON\NEXUS
python -c "from audit.daemon_phi_tracker import PhiTracker; t = PhiTracker(); import json; print(json.dumps(t.run_once(), indent=2))"
```

## Threshold
- Max .py files in NEXUS/managers/: **10** (PRD_CLARIF Phase 3 target)
- Current count: **0** (clean as of 2026-06-04)

## State File
`NEXUS/.audit/drift_watcher_state.json` tracks known file hashes.
Do not manually edit unless you understand the drift detection algorithm.
