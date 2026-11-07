---
name: kg-l-visualizer
description: Visualisation KG-L via CTULU triadic_graph_engine. Utilise ce skill quand tu dois produire un rendu Mermaid ou DOT d'un graphe causal.
trigger: kg_l_implementation
---

# KG-L Visualizer

Génère des rendus visuels de KG-L.

## Usage

```powershell
python .kilo/skills/kg-l-visualizer/visualize.py --input kg-l.json --format mermaid --output kg-l.mmd
python .kilo/skills/kg-l-visualizer/visualize.py --input kg-l.json --format dot --output kg-l.dot
```
