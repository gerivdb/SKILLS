---
name: phantom-bridge-resolver
description: "Detecte les bridges phantom dans BRIDGES.yaml, score leur utilite reelle, emet recommandation tranche (implementer / deprecier / design-backlog). Distingue les bridges declared mais sans implementation des bridges simplement defined."
version: "1.0.0"
triggers:
  - "phantom bridge"
  - "resolver phantom"
  - "bridge sans code"
  - "UAE phantom"
  - "bridge fantome"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "PHANTOM_BRIDGE", "RESOLVER"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+18 (decision UAE phantoms)"}
slotWeight: 1
trit_primitive: TritCheckConfig
---

# PHANTOM-BRIDGE-RESOLVER — Resolution des bridges fantomes

## Domaine et perimetre

Ce skill detecte les bridges declares dans BRIDGES.yaml mais sans implementation reelle (`phantom`), score leur utilite, et emet une recommandation tranchee :
- **Implementer** : use case reel, pas de doublon, code trivial
- **Deprecier** : doublon confirme, use case deja couvert
- **Design-backlog** : utile mais non prioritaire, necessite ADR

Cree comme pattern de N+18 ou 5 bridges UAE phantoms ont ete tranches (3 impl, 2 deprecated).

## Methodologie

### Phase 1 — Detecter les phantoms

```
GET gerivdb/GOVERNANCE-HUB/BRIDGES.yaml
→ Filtrer les bridges avec status: phantom
→ Pour chaque phantom, lire le champ component (fichier producteur)
```

### Phase 2 — Verifier l'existence du code

Pour chaque bridge phantom :
```
GET gerivdb/<repo>/<component_path>
→ Si 200 → le code existe → scorer pour transition defined/active
→ Si 400 → le code n'existe pas → scorer pour deprecation ou implementation
```

### Phase 3 — Scorer l'utilite reelle

Critères de scoring (0-10) :
- **Use case documente** (0-3) : Le bridge repond-il a un besoin documente dans NEXUS/EPIC ?
- **Doublon detecte** (0-3) : Un autre bridge couvre-t-il la meme fonction ?
- **Complexite d'implementation** (0-2) : Le code est-il trivial (wrapper) ou complexe ?
- **Impact downstream** (0-2) : Combien de consommateurs dependent de ce bridge ?

Score >= 7 → **Implementer**
Score 4-6  → **Design-backlog** (ADR requis)
Score < 4  → **Deprecier**

### Phase 4 — Emettre la recommandation

Pour chaque bridge :
```
[PHANTOM_RESOLVER] <bridge_id> : score=<n>/10 → <recommandation>
[PHANTOM_RESOLVER] Justification : <raison>
[PHANTOM_RESOLVER] Action : <creer code / creer ADR deprecation / backlog>
```

## Regles de decision

- **Regle 1** : Doublon confirme → Deprecier (pas de valeur ajoutee)
- **Regle 2** : Use case reel + code trivial → Implementer immediatement
- **Regle 3** : Use case flou → Design-backlog + ADR de clarification
- **Regle 4** : Jamais de deprecation sans ADR documentant la decision

## Integration

- **Declencheur** : Audit mensuel, session de gouvernance
- **Dependances** : Acces GitHub API, lecture BRIDGES.yaml + known_repositories.yaml
- **Reference ADR** : ADR-2026-06-11-001-UAE-PHANTOM-DECISION.md
- **Distingue de** : nexus-drift-scan (detecte derive de code, pas bridges non implementes)
