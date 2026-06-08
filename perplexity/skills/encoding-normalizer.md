---
skill_id: encoding-normalizer
trit_primitive: TritCheckEncoding
version: 1.1.0
updated: 2026-06-09
status: active
tags: [encoding, git, lf, crlf, filename, cross-repo]
---

# encoding-normalizer

## Purpose
Prévenir et résoudre les problèmes d'encodage LF/CRLF et de noms de fichiers avec caractères spéciaux.

## Trigger
Use when: user mentions "encoding", "LF", "CRLF", "caractères spéciaux", "accents", "accents dans noms de fichiers", or hook pre-commit blocks on encoding.

## Steps

1. **Vérifier `.gitattributes`** — assurer la configuration recommandée :
   ```
   * text=auto eol=lf
   *.md text eol=lf
   *.yaml text eol=lf
   *.py text eol=lf
   *.sh text eol=lf
   *.ps1 text eol=crlf
   *.bat text eol=crlf
   ```

2. **Détecter fichiers CRLF** :
   ```powershell
   git grep -Pl "\r" -- "*.md" "*.yaml" "*.py"
   ```

3. **Corriger** via script EPIC-A :
   ```powershell
   python scripts/governance/normalize_line_endings.py --inject
   ```

4. **Vérifier noms de fichiers** — pattern safe : `[A-Z0-9_\-\.]+` uniquement
   - Renommer tout fichier contenant accents/caractères spéciaux

## Rules
- Interdire les accents dans les noms de fichiers : `É` → `E`, `é` → `e`
- Pattern safe : `[A-Z0-9_\-\.]+` uniquement
- `.gitattributes` doit être présent dans chaque repo
- Always use `git grep -Pl` for CRLF detection — not manual inspection

## Output
- All text files use LF line endings
- All filenames match safe pattern
- `.gitattributes` configured correctly

## Example

```powershell
# Detect CRLF files
git grep -Pl "\r" -- "*.md" "*.yaml"

# Fix endings
python scripts/governance/normalize_line_endings.py --inject

# Rename problematic file
Rename-Item "PRD-DIAMOND-TERNARY-PROT\303\211OME-V1.md" "PRD-DIAMOND-TERNARY-PROTEOME-V1.md"
```

## Integration
Called automatically by hook `pre-commit` on GOVERNANCE-HUB.
