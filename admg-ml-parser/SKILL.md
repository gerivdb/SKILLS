---
name: admg-ml-parser
description: Parser EBNF v9.1 -> AST ADMG-ML. Utilise ce skill quand tu dois parser, valider ou transformer des manifests ADMG-ML.
trigger: admg_ml_langage
---

# ADMG-ML Parser

Parse la spécification EBNF v9.1 d'ADMG-ML en AST.

## Usage

```powershell
python .kilo/skills/admg-ml-parser/parser.py --input sample.admg --output ast.json
```

## Vérification

```powershell
Test-Path .kilo/skills/admg-ml-parser/SKILL.md
```
