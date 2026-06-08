---
trit_primitive: TritCheckEncoding
---
# encoding-normalizer

## Objectif
Prévenir et résoudre les problèmes d'encodage LF/CRLF et de noms de fichiers avec caractères spéciaux.

## Configuration `.gitattributes` recommandée

```
* text=auto eol=lf
*.md text eol=lf
*.yaml text eol=lf
*.py text eol=lf
*.sh text eol=lf
*.ps1 text eol=crlf
*.bat text eol=crlf
```

## Noms de fichiers
- Interdire les accents dans les noms de fichiers : `É` → `E`, `é` → `e`
- Pattern safe : `[A-Z0-9_\-\.]+` uniquement
- Exemple problématique : `PRD-DIAMOND-TERNARY-PROT\303\211OME-V1.md` → renommer en `PRD-DIAMOND-TERNARY-PROTEOME-V1.md`

## Détection
```powershell
# Détecter fichiers CRLF dans repo
git grep -Pl "\r" -- "*.md" "*.yaml" "*.py"
```

## Correction
```powershell
# Via script EPIC-A (déjà disponible)
python scripts/governance/normalize_line_endings.py --inject
```

## Intégration
Appelé automatiquement par hook `pre-commit` sur GOVERNANCE-HUB.
