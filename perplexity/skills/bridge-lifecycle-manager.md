---
name: bridge-lifecycle-manager
description: "Orchestre le cycle de vie des bridges dans BRIDGES.yaml : lecture, classification par statut (phantom/defined/active/deprecated), proposition de transitions motivees, emission patch YAML + ADR associe. Utilisable depuis Perplexity ou ENV2."
version: "1.0.0"
triggers:
  - "bridge lifecycle"
  - "transition bridge"
  - "bridges yaml update"
  - "bridge status change"
  - "activer bridge"
  - "deprecier bridge"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "BRIDGE_LIFECYCLE", "GOVERNANCE"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+13 a N+22 (8 transitions de statut)"}
slotWeight: 2
trit_primitive: TritCheckConfig
---

# BRIDGE-LIFECYCLE-MANAGER — Gestion du cycle de vie des bridges

## Domaine et perimetre

Ce skill pilote les transitions d'etat des bridges dans BRIDGES.yaml :
- `phantom` → `defined` (specification formelle)
- `defined` → `active` (code implemente + tests)
- `active` → `deprecated` (remplace ou obsolete)
- `deprecated` → `archived` (suppression confirmee)

Cree comme pattern recurrent de N+13 a N+22 ou chaque groupe d'implementation se terminait par des transitions de statut.

## Methodologie

### Phase 1 — Lire BRIDGES.yaml

```
GET gerivdb/GOVERNANCE-HUB/BRIDGES.yaml
→ Extraire tous les bridges avec leur statut actuel
→ Compter par categorie : active / defined / phantom / deprecated
```

### Phase 2 — Identifier les transitions candidates

Pour chaque bridge `defined` :
- Verifier si le fichier consumer/producer existe dans le repo cible (via GitHub API)
- Si code existe + tests existent → candidate `defined → active`
- Si code existe mais pas de tests → signaler gap

Pour chaque bridge `phantom` :
- Verifier si le fichier component existe dans le repo UAE/producteur
- Si existe → candidate `phantom → defined`
- Si n'existe pas → proposer `phantom → deprecated` ou implementation

Pour chaque bridge `active` :
- Verifier si un bridge alternatif le remplace (doublon)
- Si doublon confirme → candidate `active → deprecated`

### Phase 3 — Emettre le patch

Pour chaque transition valide :
1. Modifier le champ `status` dans BRIDGES.yaml
2. Mettre a jour les compteurs `meta.active_count`, `meta.defined_count`, etc.
3. Emettre le commit via MCP push_files
4. Si transition vers `deprecated`, creer l'ADR de deprecation

### Phase 4 — Rapport

```
[BRIDGE_LIFECYCLE] Transitions proposees : N
[BRIDGE_LIFECYCLE] defined → active : N
[BRIDGE_LIFECYCLE] phantom → defined : N
[BRIDGE_LIFECYCLE] phantom → deprecated : N
[BRIDGE_LIFECYCLE] active → deprecated : N
[BRIDGE_LIFECYCLE] BRIDGES.yaml version : X.Y.Z → X.Y.Z+1
```

## Regles de decision

- **Regle 1** : `defined → active` requiert code + tests dans le repo cible
- **Regle 2** : `phantom → deprecated` si aucun code UAE trouve ET doublon confirme
- **Regle 3** : `active → deprecated` uniquement si bridge alternatif actif existe
- **Regle 4** : Ne jamais archiver sans ADR de deprecation
- **Regle 5** : Mettre a jour `meta.last_updated` a chaque patch

## Integration

- **Declencheur** : Fin de session d'implementation, audit mensuel
- **Dependances** : Acces GitHub API pour verifier l'existence des fichiers
- **Reference ADR** : ADR-2026-06-11-001-UAE-PHANTOM-DECISION.md
