---
name: phi-cps-aggregator
description: "Depuis Perplexity, pilote ARGUS pour lancer un cycle phi_aggregate, lire le rapport phi_ecosystem.json, interpreter les resultats, identifier les repos sous le seuil, emettre les recommandations ADR."
version: "1.0.0"
triggers:
  - "phi aggregate"
  - "phi cps"
  - "audit phi"
  - "ecosystem health"
  - "phi_ecosystem"
layer: "L1_CAUSALITY"
nexusTags: ["CONFORME_NEXUS", "PHI_CPS", "AGGREGATOR"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+13 (phi_aggregate.py)"}
slotWeight: 1
trit_primitive: TritAnalyzeConfig
---

# PHI-CPS-AGGREGATOR — Aggregation phi_cps multi-repos

## Domaine et perimetre

Ce skill pilote le cycle d'audit phi_cps depuis Perplexity : lancement du scan ARGUS, lecture du rapport, interpretation, recommandations.

## Methodologie

### Phase 1 — Lancer le cycle

```
POST ARGUS/engines/phi_aggregate.py
→ Scanner tous les repos actifs
→ Calculer phi_cps par repo
→ Produire reports/phi_ecosystem.json
```

### Phase 2 — Lire le rapport

```
GET ARGUS/reports/phi_ecosystem.json
→ phi_ecosystem (score global)
→ phi_integrated (boolean)
→ vote_coherence_score
→ repos_contributors[]
```

### Phase 3 — Interpreter

- Score global < 3.5 → ECOSYSTEM DEGRADE
- Repos sous seuil → identifier les contributeurs faibles
- Vote coherence < 0.5 → DISCORDANCE

### Phase 4 — Recommandations

Pour chaque repo sous seuil :
- Creer issue GitHub avec tag PHI_DEGRADATION
- Proposer ADR si degradation confirmee
- Planifier session de remediation

## Integration

- **Declencheur** : Cron 6h, audit mensuel
- **Dependances** : Acces ARGUS, GitHub API
