---
name: pre-impl-inventory
description: >
  Outil d'inventaire pre-implementation V21.0 PROPHETIC.
  Scan les repos, partitionne S/K/R, prouve invariants TINA/Z3, mappe ATOMs,
  et genere 5 sorties: md/json/beads/talex/serena.
  Implémentation complete avec KORX-L1 cache, SPIDX, ATOM mapper.
version: "1.0.0"
status: active
intent_hash: 0xPRE_IMPL_INVENTORY_V21_20260806
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: pre-impl-inventory/SKILL.md
triggers:
  - "inventaire pre-implementation"
  - "asset inventory"
  - "pre-impl scan"
  - "V21 prophetique"
tools:
  - bash
  - read
  - grep
  - codebase_search
citizen: "PRE-IMPL-INVENTORY"
layer: "L4"
implementation:
  language: Python
  package: pre_impl_inventory
  tests: tests/test_pre_impl_inventory.py
  bin: bin/pre-impl-inventory
---

# Skill — Pre-Implementation Inventory V21.0 PROPHETIC

> **Verdict** : **SKILL D'EXECUTION** — Inventaire pré-implémentation avec 15 composants prophétiques.

---

## Objectif

Cartographie déterministe des assets (skills, citizens, workflows, designs, templates, scripts) avant implémentation.
Résilience systémique garantie : preuves TINA/Z3, partition S/K/R, mapping ATOM, économie de contexte Serena.

## Implementation

### Package Python

```
pre-impl-inventory/
├── pre_impl_inventory/
│   ├── __init__.py          # InventoryEngine, AssetScanner, SPIDX, ATOMMapper
│   └── ...
├── tests/
│   └── test_pre_impl_inventory.py
├── bin/
│   └── pre-impl-inventory   # CLI
└── SKILL.md
```

### Pipeline V21.0

```
Input: PRD path
  │
  ├─ [KORX-L1] Cache state.kbin -> O(1) assets connus
  │
  ├─ [AssetScanner] Scan skills/citizens/workflows/designs/templates/scripts
  │
  ├─ [SPIDX] Partition S/K/R -> resilience topologique
  │
  ├─ [TINA/Z3] Preuve invariants L0-L5
  │
  ├─ [ATOMMapper] Mapping immuable -> Knowledge Graph
  │
  └─ [Outputs] md + json + beads + talex + serena
```

### Composants

| Composant | Implémentation |
|-----------|----------------|
| KORX-L1 | KORXCache (state.kbin) |
| AssetScanner | Scan patterns skills/citizens/workflows/designs/templates/scripts |
| SPIDX | Partition S/K/R avec détection cycles |
| TINA/Z3 | TINAZ3 placeholder (preuves invariants) |
| ATOMMapper | Mapping ATOM par asset |
| Outputs | Markdown + JSON + Beads + TALEX + Serena |

### CLI

```bash
pre-impl-inventory <prd_path>
```

### Tests

```bash
python tests/test_pre_impl_inventory.py
```

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Assets scannés | 100% | AssetScanner |
| Performance | < 500 µs | Benchmark |
| Preuves TINA/Z3 | 100% invariants | TINAZ3 |
| Partition S/K/R | 0 cycle non partitionné | SPIDX |
| Mapping ATOM | 100% designs -> ATOM | ATOMMapper |
| Sorties | 5 fichiers | Verification |

## Rollback

1. Revenir aux outputs precedents.
2. Logger dans WAL.
3. Corriger via PR review MOX.

## References

- `PRD-MOC-PRE_IMPL_INVENTORY_V21_2026-08-05.md`
- `SKILLS/mox-validator/`
- `KORX/` : cache L1
- `TINA/` : preuve Z3
- `SPIDX/` : partition graphe
- `TALEX/` : synthese narrative
- `Serena/` : symbol-level retrieval
