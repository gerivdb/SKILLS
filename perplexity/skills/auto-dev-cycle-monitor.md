---
name: auto-dev-cycle-monitor
description: "Lit NEXUS/auto-dev/cycles/, verifie les transitions P1->P7, detecte les blocages FLUX, audite les logs MIMIR DISCOVERY_LOG.md. Outil de supervision AUTO-DEV depuis Perplexity."
version: "1.0.0"
triggers:
  - "auto dev cycle"
  - "cycle P1 P7"
  - "AUTO-DEV monitor"
  - "MIMIR discovery"
  - "FLUX gate status"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "AUTO_DEV", "MONITOR"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+19 (5 bridges AUTO-DEV)"}
slotWeight: 1
trit_primitive: TritCheckConfig
---

# AUTO-DEV-CYCLE-MONITOR — Supervision des cycles AUTO-DEV

## Domaine et perimetre

Ce skill supervise les cycles AUTO-DEV depuis Perplexity : lecture des cycles NEXUS, verification des transitions P1→P7, detection des blocages FLUX, audit MIMIR.

## Methodologie

### Phase 1 — Lire les cycles

```
GET gerivdb/NEXUS/auto-dev/cycles/
→ Lister les fichiers CYCLE-{n}-{date}.yaml
→ Parser les phases, timestamps, status
```

### Phase 2 — Verifier les transitions

Pour chaque cycle :
- Phase actuelle vs phase attendue
- Derniere transition timestamp
- Si blocage > 48h → alerter

### Phase 3 — Auditer FLUX gate

```
GET gerivdb/AUTO-DEV/agents/flux_gate.py
→ Verifier HITL_APPROVED status
→ Lister les gates en attente
```

### Phase 4 — Lire MIMIR

```
GET gerivdb/MIMIR/DISCOVERY_LOG.md
→ Parser les dernieres decouvertes
→ Identifier les P6 completes
```

## Integration

- **Declencheur** : Supervision quotidienne, audit de session
- **Dependances** : Acces GitHub API (NEXUS, AUTO-DEV, MIMIR)
