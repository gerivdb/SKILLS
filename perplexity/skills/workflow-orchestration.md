---
trit_primitive: TritDocumentTrace
---
# WAZAA Dynamic Workflow Orchestration -- Skill Reference
# IntentHash: 0xSKILL_WAZAA_WORKFLOWS_20260603
# Source: PRD_DYNAMIC_WORKFLOW_ORCHESTRATION_V1

## Overview

This skill documents the 3 recurring workflows wired via WAZAA bus
during PRD_ORCH Sprints 1-4.

## Workflow 1: Triade Cognitive Signal Routing

**Trigger:** IRIS cron poll (6h) or manual trigger
**Path:** IRIS -> WAZAA -> KRONOS -> Route to ECOS-CLI | KIVA | BRAIN

```
IRIS.poll() -> iris.signal.raw -> KRONOS.qualify() -> kronos.signal.qualified
  score < 3  -> ECOS-CLI
  score 3-6  -> KIVA
  score > 6  -> BRAIN
```

**Files:**
- `IRIS/src/wazaa_client.py` -- IRIS WAZAA client
- `KRONOS/src/wazaa_client.py` -- KRONOS WAZAA client with routing
- `KRONOS/src/qualifier.py` -- Heuristic scoring
- `WAZAA/contracts/event_schema.yaml` -- Event topic definitions

## Workflow 2: KIVA Fan-out Audit with Barrier

**Trigger:** KRONOS-qualified signal (score 3-6) or manual trigger
**Path:** KIVA -> fan-out to N repos -> barrier -> BRAIN synthesis

```
KIVA.fanout_start() -> kiva.fanout.start
  -> parallel audit on N repos -> kiva.fanout.result (per repo)
  -> kiva.fanout.barrier (all collected)
  -> kiva.goal.eval (hard-stop check)
  -> BRAIN.synthesize()
```

**Hard-stop condition:** NEXUS/managers/ Python files <= 10

**Files:**
- `KIVA/src/scheduler.py` -- FanoutBarrier, KivaGoal, loop_until_done
- `KIVA/src/wazaa_client.py` -- KIVA WAZAA client

## Workflow 3: BRAIN/FLUENCE Generate-Filter

**Trigger:** High-priority signal (score > 6) or manual trigger
**Path:** BRAIN -> FLUENCE -> KRONOS filter

```
BRAIN.generate(N=5) -> brain.generate.result
  -> FLUENCE.score(phi) -> fluence.score
  -> KRONOS.filter(phi >= 4.0) -> fluence.filter
  -> Surviving options promoted
```

**Files:**
- `WAZAA/contracts/generate_filter_pipeline.py` -- Pipeline implementation

## BLO Tournament

**Trigger:** Multi-agent decision required
**Path:** BLO -> tournament -> winner + synthesis

```
BLO.start() -> blo.tournament.start
  -> rounds -> blo.tournament.round
  -> finalize -> blo.tournament.result (winner + synthesis)
```

**Files:**
- `WAZAA/contracts/blo_tournament.py` -- Tournament orchestrator

## Event Schema

All events conform to `WAZAA/contracts/event_schema.yaml`.
All agents connect via `wazaa_client.py` in their respective `src/` directories.
