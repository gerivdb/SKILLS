---
name: admg-ml-doc-generator
description: Génération automatique de documentation ADMG-ML. Utilise ce skill quand tu dois produire la doc utilisateur depuis les manifests YAML + EBNF.
trigger: admg_ml_langage
---

# ADMG-ML Doc Generator

Génère la documentation ADMG-ML depuis les manifests YAML et l'EBNF.

## Usage

```powershell
python .kilo/skills/admg-ml-doc-generator/generate.py --input manifests/ --output docs/
```
