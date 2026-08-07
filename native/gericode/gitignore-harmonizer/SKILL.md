---
name: gitignore-harmonizer
description: "Harmonise les .gitignore pour supporter Hexagonal/BDD/ATDD sans git add -f."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_GITIGNORE_HARMONIZER_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/gitignore-harmonizer/SKILL.md
triggers:
  - "harmonize gitignore"
  - "fix gitignore"
  - "gitignore audit"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - gitignore-harmonizer

> **Verdict** : **SKILL D'EXECUTION** - Harmonise les `.gitignore`.

---

## Objectif

Remplacer les patterns trop larges par des patterns precis pour supporter Hexagonal/BDD/ATDD.

---

## Declencheur

- Nouveau skill avec structure Hexagonal
- Ajout de repertoires `out/`, `infrastructure/adapters/`
- CI/CD : detection de `git add -f` necessaire

---

## Patterns a corriger

```
# [KO] AVANT
out/
infrastructure/adapters/

# [OK] APRES
infrastructure/adapters/out/
infrastructure/adapters/in/
tests/__pycache__/
.kilo/__pycache__/
```

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `repo_path` | Path | Chemin du repo |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `report` | dict | Rapport d'harmonisation |
 | `fixed` | list | Fichiers modifies |
 | `errors` | list | Erreurs |

---

## Regles

1. Jamais `out/` seul (trop large)
2. Jamais `infrastructure/adapters/` (bloque Hexagonal)
3. Autoriser explicitement `infrastructure/adapters/in/` et `infrastructure/adapters/out/`
4. `__pycache__/` autorise seulement dans `.kilo/skills/*/` et `tests/`

---

## Exemple d'usage

```python
from pathlib import Path
from gitignore_harmonizer import GitignoreHarmonizer

harmonizer = GitignoreHarmonizer(repo_path=Path("."))
report = harmonizer.harmonize(dry_run=False)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_harmonize_gitignore` | Correction patterns | Patterns corriges |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |
 | `test_detect_broad_patterns` | Detection patterns larges | Patterns detectes |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-908    Aucun .gitignore ne contient le pattern `out/` seul                |
 | P-909    infrastructure/adapters/in/ et out/ ne sont pas ignores           |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          gitignore-harmonizer fonctionne                                  |
 | [OK]          P-908 passe                                                      |
 | [OK]          P-909 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `.gitignore` de GeriCode
