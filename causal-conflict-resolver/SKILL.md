---
name: causal-conflict-resolver
description: Résolution de conflits causaux entre graphes ADMG-ML. Utilise ce skill quand tu dois merger deux graphes causaux avec contradictions.
trigger: kg_l_implementation
---

# Causal Conflict Resolver

Résout les conflits entre graphes causaux.

## Usage

```powershell
python .kilo/skills/causal-conflict-resolver/resolve.py --left left.json --right right.json --output merged.json
```
