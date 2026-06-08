---
name: uae-keel-coords
version: "1.0.0"
description: "Génération de coords.yaml + graph.yaml pour les skills UAE. Formule embedding 1/√d, zones LADYBIRD/STANDARD/BASIC, 5 axes UAE (strate/domaine/env/phase/urgence). Utiliser quand l'utilisateur mentionne 'coordonner les skills', 'UAE layout', 'coords.yaml', 'graph.yaml UAE', 'KEEL functor'."
triggers:
  - "coordonner les skills"
  - "UAE layout"
  - "coords.yaml"
  - "graph.yaml UAE"
  - "KEEL functor"
  - "UAE score"
  - "LADYBIRD zone"
layer: "L1_SOT"
nexusTags: ["CONFORME_NEXUS", "UAE", "KEEL"]
prerequisites:
  - "gerivdb/SKILLS/MANIFEST.json"
  - "gerivdb/SKILLS/TAXONOMY/ (template)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — UAE coords + KEEL graph"}
trit_primitive: TritIsolate
---

# UAE-KEEL-COORDS — Coordonnées UAE + Graphe KEEL

## Domaine et périmètre

Ce skill génère et maintient les fichiers `coords.yaml` et `graph.yaml` qui définissent les coordonnées UAE de chaque skill et les foncteurs KEEL entre eux.

## Les 5 axes UAE

| Axe | Valeurs | Description |
|-----|---------|-------------|
| strate | L0-L9 | Strate écosystème (L0=gouvernance, L4=orchestration, L5=meta) |
| domaine | governance/sot/cognition/automation/git/agentic/domain/external | Domaine fonctionnel |
| env | ENV1/ENV2/BOTH | Environnement cible |
| phase | create/audit/fix/close/route | Phase du cycle de vie |
| urgence | P0-P3 | Priorité opérationnelle |

## Score UAE

Formule : `score = 100 * (1 - d_min / d_max)`

Où :
- `d_min` = distance euclidienne au centre UAE le plus proche
- `d_max` = distance maximale possible (√124 ≈ 11.1)

Centres multi-pôles :
- `(0, 0, 1, 1, 1)` — L0 governance audit P1
- `(4, 5, 1, 4, 0)` — L4 agentic route P0

## Zones

| Zone | Score | Signification |
|------|-------|---------------|
| LADYBIRD | ≥ 80 | Skill prioritaire — cœur de l'écosystème |
| STANDARD | 60-79 | Skill normal |
| BASIC | < 60 | Skill optionnel |

## Génération automatique

```bash
python scripts/generate_coords.py
python scripts/generate_coords.py --check  # idempotence
```

## Format coords.yaml

```yaml
skills:
  skill-name:
    strate: L0
    domaine: governance
    env: BOTH
    phase: audit
    urgence: P1
    uae_score: 78.5
    zone: STANDARD
```

## Format graph.yaml

```yaml
adjunctions:
  skill-source:
    adjoints:
      - skill: skill-target
        condition: "strate == L0"
        cost: 0.1
        functor: "𝔽|source→target"
    composition: "≋"
    identite: "≋"
```

## Intégration

- **Dépôts** : SKILLS (TAXONOMY/), BRAIN (KEEL parser)
- **Couche EECS** : L1_SOT
- **Skills dépendants** : skills-agentic (DELEGATOR route via UAE)
