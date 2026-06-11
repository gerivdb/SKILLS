---
name: multi-agent-consumer-orchestrator
description: "A partir d'une source de signal (TOPOS/WAL/drift/pattern), identifie tous les agents consumers declares dans BRIDGES.yaml, verifie leur statut, orchestre leur invocation, consolide les rapports. Pattern fan-out consumer."
version: "1.0.0"
triggers:
  - "orchestrer consumers"
  - "fan out consumer"
  - "multi agent consumer"
  - "TOPOS consumers"
  - "WAL consumers"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "ORCHESTRATOR", "FAN_OUT"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+16 (4 agents TOPOS en parallele)"}
slotWeight: 2
trit_primitive: TritDoConfig
---

# MULTI-AGENT-CONSUMER-ORCHESTRATOR — Orchestration fan-out des consumers

## Domaine et perimetre

Ce skill orchestre l'invocation de multiples agents consommateurs a partir d'une source de signal commune. Le pattern a ete detecte dans N+16 ou 4 agents (SABRE, MirrorFish, CoPaw, Alfred) consommaient la meme source TOPOS en parallele.

## Methodologie

### Phase 1 — Identifier la source

Sources supportees :
- **TOPOS** : `envs/*/topos.yaml`
- **WAL** : `wal/` events (diff0-fork, diffscope)
- **Drift** : ARGUS drift reports
- **Pattern** : diffscope pattern signals

### Phase 2 — Identifier les consumers

```
GET gerivdb/GOVERNANCE-HUB/BRIDGES.yaml
→ Filtrer les bridges avec consumer.repo = <agent>
→ Lister les consumers par source
→ Verifier leur statut (active/defined)
```

### Phase 3 — Orchestrer l'invocation

Pour chaque consumer actif :
1. Charger la source de signal
2. Invoquer le consumer (`load_topos()` / `consume_event()`)
3. Collecter le rapport
4. Consolider

Supporte deux modes :
- **Sequentiel** : un par un (safe, lent)
- **Parallele** : tous simultanement (rapide, necessite RAM)

### Phase 4 — Consolider les rapports

```
[MULTI_CONSUMER] Source: <source>
[MULTI_CONSUMER] Consumers invoques: N
[MULTI_CONSUMER] Rapports consolidés: N
[MULTI_CONSUMER] Alertes: <liste>
```

## Regles de decision

- **Regle 1** : Ne pas invoquer les consumers `defined` (code incomplet)
- **Regle 2** : En mode parallele, limiter a 3 consumers simultanes (RAM)
- **Regle 3** : Consolider les alertes par severite

## Integration

- **Declencheur** : Cycle de signal (TOPOS scan, WAL event, drift detection)
- **Dependances** : Acces GitHub API, BRIDGES.yaml
- **Pattern source** : N+16 (4 agents TOPOS)
