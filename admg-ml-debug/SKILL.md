---
name: admg-ml-debug
description: Debugger interactif ADMG-ML : AST, DAG, preuves SPIDX. Utilise ce skill quand tu dois inspecter ou débugger un pipeline ADMG-ML.
trigger: admg_ml_langage
---

# ADMG-ML Debug

Inspecte l'AST, les DAG et les preuves SPIDX d'ADMG-ML.

## Usage

```powershell
python .kilo/skills/admg-ml-debug/debug.py --input sample.admg --mode ast
python .kilo/skills/admg-ml-debug/debug.py --input kg-l.json --mode dag
```
