---
name: admg-ml-lint
description: Lint des manifests YAML ADMG-ML. Utilise ce skill quand tu dois vérifier la syntaxe et la sémantique des fichiers ADMG-ML.
trigger: admg_ml_langage
---

# ADMG-ML Lint

Vérifie la conformité des manifests YAML ADMG-ML.

## Usage

```powershell
python .kilo/skills/admg-ml-lint/lint.py --input manifests/
```

## Vérification

```powershell
Test-Path .kilo/skills/admg-ml-lint/SKILL.md
```
