---
name: kg-l-builder
description: Construction KG-L depuis TALEX UnifiedSemanticGraph. Utilise ce skill quand tu dois créer ou étendre le Knowledge Graph causal.
trigger: kg_l_implementation
---

# KG-L Builder

Construit KG-L en étendant TALEX UnifiedSemanticGraph avec EdgeKind causaux.

## Usage

```powershell
python .kilo/skills/kg-l-builder/build.py --source TALEX --output kg-l.json
```

## Vérification

```powershell
Test-Path .kilo/skills/kg-l-builder/SKILL.md
```
