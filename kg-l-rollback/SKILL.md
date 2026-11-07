---
name: kg-l-rollback
description: Rollback KG-L depuis SPIDX/WAL. Utilise ce skill quand tu dois restaurer une version antérieure du graphe KG-L.
trigger: kg_l_implementation
---

# KG-L Rollback

Restaure une version précédente de KG-L depuis SPIDX/WAL.

## Usage

```powershell
python .kilo/skills/kg-l-rollback/rollback.py --target <proof_id> --output kg-l.json
```
