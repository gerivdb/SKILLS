# Agent Health Check Skill

## Purpose
Verify the health of all 7 registered agents and report status.

## When to Use
- Before starting a new session
- After deploying new agents
- When debugging inter-agent communication issues
- Periodic health audit (recommended: daily)

## Workflow

### Step 1: Run health pulse check
```bash
cd D:\DO\WEB\TOOLS\L3-CITIZENS\AGENT-REGISTRY
python -c "from src.daemon_health_pulse import AgentHealthPulse; d = AgentHealthPulse(); import json; print(json.dumps(d.run_once(), indent=2))"
```

### Step 2: Interpret results
- `HEALTHY`: Agent has written a heartbeat within 60s
- `STALE`: Agent heartbeat is older than 60s
- `SILENT`: Agent has never written a heartbeat

### Step 3: For SILENT agents, check
1. Is the agent repo present?
2. Has the agent been started?
3. Is the `.agent/` directory writable?

### Step 4: Write heartbeat (if agent is running)
```python
from src.daemon_health_pulse import write_heartbeat
from pathlib import Path
write_heartbeat(Path(r"<agent_path>"), version="1.0.0")
```

## Expected Output
```json
{
  "timestamp": "2026-06-04T00:00:00+00:00",
  "total_agents": 7,
  "healthy": 0,
  "stale": 0,
  "silent": 7,
  "agents": {
    "ARGUS": {"status": "SILENT", "last_seen": null, "age_seconds": null},
    "KRONOS": {"status": "SILENT", "last_seen": null, "age_seconds": null},
    ...
  }
}
```

## Agent Registry Reference
| Agent | Path | Layer |
|-------|------|-------|
| ARGUS | `D:\DO\WEB\TOOLS\L3-CITIZENS\ARGUS` | L1_CAUSALITY |
| KRONOS | `D:\DO\WEB\TOOLS\L3-CITIZENS\KRONOS` | L3_EMERGENCE |
| IRIS | `D:\DO\WEB\TOOLS\L3-CITIZENS\IRIS` | L3_EMERGENCE |
| KIVA | `D:\DO\WEB\TOOLS\L1-INFRA\KIVA` | L1_CAUSALITY |
| BRAIN | `D:\DO\WEB\TOOLS\L0-CANON\BRAIN` | L3_EMERGENCE |
| FLUENCE | `D:\DO\WEB\TOOLS\L1-INFRA\FLUENCE` | L3_EMERGENCE |
| WAZAA | `D:\DO\WEB\TOOLS\L3-CITIZENS\WAZAA` | L3_EMERGENCE |
