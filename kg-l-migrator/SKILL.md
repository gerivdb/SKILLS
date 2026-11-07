---
name: kg-l-migrator
description: Migration TALEX -> KG-L avec EdgeKind causaux. Utilise ce skill quand tu dois migrer un graphe TALEX existant vers KG-L.
trigger: kg_l_implementation
---

# KG-L Migrator

Migre TALEX UnifiedSemanticGraph vers KG-L avec arêtes causales.

## Usage

```powershell
python .kilo/skills/kg-l-migrator/migrate.py --source talex-graph.json --output kg-l.json
```
