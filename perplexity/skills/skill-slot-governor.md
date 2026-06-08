---
name: skill-slot-governor
version: "1.0.0"
description: "Gestion du budget 100 slots SKILLS : audit courant, projection, règles LADYBIRD/STANDARD/BASIC, anti-dépassement. Utiliser quand l'utilisateur mentionne 'combien de slots restants', 'peut-on ajouter un skill', 'budget slots', 'slot count', 'MANIFEST.json'."
triggers:
  - "combien de slots restants"
  - "peut-on ajouter un skill"
  - "budget slots"
  - "slot count"
  - "MANIFEST.json"
  - "skillsCount"
layer: "L0_GOVERNANCE"
nexusTags: ["CONFORME_NEXUS", "GOVERNANCE"]
prerequisites:
  - "gerivdb/SKILLS/MANIFEST.json"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — gestion du budget 100 slots"}
trit_primitive: TritHierarchize
---

# SKILL-SLOT-GOVERNOR — Gestion du budget 100 slots

## Domaine et périmètre

Ce skill gère le **budget de 100 slots** du repo SKILLS. Il audite l'état courant, projette l'impact d'ajouts, et bloque les dépassements.

## Règles

| Règle | Description |
|-------|-------------|
| Plafond | Maximum 100 skills dans le registre Perplexity |
| Slot weight | Chaque skill consomme 1 slot (par défaut) |
| Zone LADYBIRD | Score UAE ≥ 80 — skill prioritaire |
| Zone STANDARD | Score UAE 60-79 — skill normal |
| Zone BASIC | Score UAE < 60 — skill optionnel |

## Audit courant

```bash
python tools/check-slots.py --max 100
```

Ou manuellement :
```python
import json
with open('MANIFEST.json') as f:
    m = json.load(f)
print(f"Skills: {m['skillsCount']}/100")
print(f"Marge: {100 - m['skillsCount']}")
```

## Projection d'ajout

Avant d'ajouter un skill :
1. Vérifier `skillsCount` actuel
2. Calculer `100 - skillsCount` = marge restante
3. Si marge ≤ 0 → **BLOQUÉ** — archiver un skill existant d'abord
4. Si marge ≤ 5 — **ALERTE** — budget critique
5. Si marge > 5 — **OK** — ajout autorisé

## Commandes de vérification

```bash
# Vérifier le slot count
python -c "import json; m=json.load(open('MANIFEST.json')); print(f'{m[\"skillsCount\"]}/100')"

# Lister les skills par zone
python tools/check-slots.py --zones
```

## Intégration

- **Dépôts** : SKILLS (MANIFEST.json)
- **Couche EECS** : L0_GOVERNANCE
- **Tags NEXUS** : [CONFORME_NEXUS], [GOVERNANCE]
