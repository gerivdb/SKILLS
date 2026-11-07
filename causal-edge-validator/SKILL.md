---
name: causal-edge-validator
description: Validation des arêtes causales causes/confounds/prevents. Utilise ce skill quand tu dois valider un DAG/ADMG KG-L.
trigger: kg_l_implementation
---

# Causal Edge Validator

Valide les arêtes causales selon le typage ADMG.

## Usage

```powershell
python .kilo/skills/causal-edge-validator/validate.py --input kg-l.json
```

## Vérification

```powershell
Test-Path .kilo/skills/causal-edge-validator/SKILL.md
```
