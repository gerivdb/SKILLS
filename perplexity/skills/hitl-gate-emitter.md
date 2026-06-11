---
name: hitl-gate-emitter
description: "A partir du recapitulatif d'un groupe d'implementation (fichiers crees, repos, date), genere automatiquement le fichier JSON de gate FLUX avec le bon schema et le pousse dans GOVERNANCE-HUB."
version: "1.0.0"
triggers:
  - "emettre gate FLUX"
  - "gate HITL"
  - "creer gate"
  - "FLUX review"
  - "session closeout gate"
layer: "L3_CITIZENS"
nexusTags: ["CONFORME_NEXUS", "HITL", "FLUX_GATE"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern repete a chaque groupe N+13 a N+22"}
slotWeight: 1
trit_primitive: TritNotify
---

# HITL-GATE-EMITTER — Emission des gates FLUX

## Domaine et perimetre

Ce skill genere automatiquement le fichier JSON de gate FLUX a partir du recapitulatif d'un groupe d'implementation. Le pattern a ete repete a chaque groupe N+13 a N+22.

## Schema du fichier gate

```json
{
  "gate_id": "N<nn>-<slug>",
  "group_number": "<n>",
  "timestamp": "<ISO 8601>",
  "status": "pending",
  "files_created": ["<path>", ...],
  "repos_affected": ["<repo>", ...],
  "bridges_transitionned": ["<bridge_id>", ...],
  "adr_created": ["<adr_path>", ...],
  "tests_created": ["<test_path>", ...],
  "hitl_required": true,
  "reviewer": null,
  "reviewed_at": null,
  "decision": null
}
```

## Methodologie

### Phase 1 — Collecter le recapitulatif

A partir du bilan de session :
- Numero de groupe (N+<n>)
- Fichiers crees (paths)
- Repos affectes
- Bridges transitionnes
- ADR crees

### Phase 2 — Generer le fichier

1. Construire le JSON avec le schema ci-dessus
2. Nommer le fichier `N<nn>-<slug>.slug` (ex: `N13-argus-diff0.json`)
3. Ecrire dans `FLUX/reviews/pending/`

### Phase 3 — Pousser

```
PUT gerivdb/GOVERNANCE-HUB/FLUX/reviews/pending/N<nn>-<slug>.json
```

## Regles de decision

- **Regle 1** : Un fichier gate par groupe d'implementation
- **Regle 2** : Le slug est derive du contenu (ex: "argus-diff0", "tina-verses")
- **Regle 3** : Status initial = "pending"
- **Regle 4** : Distinct de hitl-core (qui documente le concept, pas l'emission)

## Integration

- **Declencheur** : Fin de chaque groupe d'implementation
- **Dependances** : Acces GitHub API (GOVERNANCE-HUB)
- **Complementaire de** : hitl-core, session-closeout
