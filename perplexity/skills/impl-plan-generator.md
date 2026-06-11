---
name: impl-plan-generator
description: "Charge un registre d'etat (BRIDGES.yaml, EPIC catalog, known_repositories.yaml), calcule les gaps, genere un plan d'implementation groupe + sequence avec estimation duree, fichiers cibles, repos, strate L, gate HITL. Utilisable depuis Perplexity."
version: "1.0.0"
triggers:
  - "generer plan implementation"
  - "plan NEXUS"
  - "implementation plan"
  - "gap analysis"
  - "planifier implementation"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "IMPL_PLAN", "GENERATOR"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans plan N+13 a N+22"}
slotWeight: 2
trit_primitive: TritThinkConfig
---

# IMPL-PLAN-GENERATOR — Generation de plans d'implementation

## Domaine et perimetre

Ce skill charge un registre d'etat, calcule les gaps entre l'etat actuel et l'etat cible, et genere un plan d'implementation structure en groupes sequentiels.

Cree comme pattern de la premiere partie de la session N+13→N+22 ou un plan complet a ete genere depuis l'analyse de BRIDGES.yaml.

## Methodologie

### Phase 1 — Charger les registres

```
GET gerivdb/GOVERNANCE-HUB/BRIDGES.yaml
GET gerivdb/GOVERNANCE-HUB/known_repositories.yaml
GET gerivdb/GOVERNANCE-HUB/EPICs/
→ Parser les statuts, les gaps, les dependances
```

### Phase 2 — Calculer les gaps

Pour chaque bridge `defined` ou `phantom` :
- Fichier producteur existe-t-il ?
- Fichier consumer existe-t-il ?
- Tests existent-ils ?
- ADR de reference existe-t-il ?

Classifier les gaps par priorite :
- **HAUTE** : Code manquant + impact downstream multiple
- **MOYENNE** : Code manquant + impact limite
- **BASSE** : Tests manquants ou documentation incomplete

### Phase 3 — Generer le plan

Structurer en groupes sequentiels :
```
Groupe 1 — Bridges critiques (deblocage downstream)
  N+<n> : <bridge_id> — <description courte>
    Fichiers : <liste>
    Repos : <liste>
    Duree estimee : <n> sessions
    Gate HITL : <oui/non>

Groupe 2 — Bridges secondaires
  ...
```

### Phase 4 — Estimer la charge

Par groupe :
- Nombre de fichiers a creer
- Nombre de repos concernes
- Duree estimee (en sessions de travail)
- Gates HITL requises

## Format de sortie

```
PLAN D'IMPLEMENTATION — <date>
================================
Registre source : BRIDGES.yaml v<version>
Bridges analyses : <n>
Gaps identifies : <n>

GROUPE 1 — <nom> (<n> bridges)
  N+<n> : <action>
    Fichiers : <n>
    Repos : <n>
    Duree : <n> sessions

[...]

Total : <n> fichiers de code + <n> gates HITL
Couverture finale estimee : <n>%
```

## Integration

- **Declencheur** : Debut de session de gouvernance, audit trimestriel
- **Dependances** : Acces GitHub API pour verifier l'existence des fichiers
- **Complementaire de** : bridge-lifecycle-manager (execute les transitions)
