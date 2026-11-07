---
name: causal-graph-diff
description: Diff de graphes causaux pour SPIDX. Utilise ce skill quand tu dois comparer deux versions de graphe causal.
trigger: spidx_evidence
---

# Causal Graph Diff

Génère un diff de graphes causaux pour les preuves SPIDX.

## Usage

```powershell
python .kilo/skills/causal-graph-diff/diff.py --before before.json --after after.json --output diff.spidx
```
