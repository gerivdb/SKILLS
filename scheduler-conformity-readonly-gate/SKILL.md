---
name: scheduler-conformity-readonly-gate
description: Gate fail-closed: si Shard E échoue, les autres shards passent en readonly.
version: 1.0.0
status: stable
canonical: true
legacy_path: skills/scheduler-conformity-readonly-gate
---
# scheduler-conformity-readonly-gate

Gate fail-closed: si Shard E échoue, les autres shards passent en readonly.

## Source
- source_file: shard_scheduler.py
- legacy_path: skills/scheduler-conformity-readonly-gate (canonisé vers racine L4-TOOLS/SKILLS/scheduler-conformity-readonly-gate)

## Triggers / usage
Voir SKILL.yaml (triggers déclaratifs). Référencé par citizens ENV3 (contrat skill-name).