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

# Skill — gitignore-harmonizer

> **Verdict** : **SKILL D'EXÉCUTION** — Harmonise les `.gitignore`.

---

## Objectif

Remplacer les patterns trop larges par des patterns précis pour supporter Hexagonal/BDD/ATDD.

---

## Déclencheur

- Nouveau skill avec structure Hexagonal
- Ajout de répertoires `out/`, `infrastructure/adapters/`
- CI/CD : détection de `git add -f` nécessaire

---

## Patterns à corriger

```
# ❌ AVANT
out/
infrastructure/adapters/

# ✅ APRÈS
infrastructure/adapters/out/
infrastructure/adapters/in/
tests/__pycache__/
.kilo/__pycache__/
```

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `repo_path` | Path | Chemin du repo |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `report` | dict | Rapport d'harmonisation |
 | `fixed` | list | Fichiers modifiés |
 | `errors` | list | Erreurs |

---

## Règles

1. Jamais `out/` seul (trop large)
2. Jamais `infrastructure/adapters/` (bloque Hexagonal)
3. Autoriser explicitement `infrastructure/adapters/in/` et `infrastructure/adapters/out/`
4. `__pycache__/` autorisé seulement dans `.kilo/skills/*/` et `tests/`

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
 | `test_harmonize_gitignore` | Correction patterns | Patterns corrigés |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |
 | `test_detect_broad_patterns` | Détection patterns larges | Patterns détectés |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-908    Aucun .gitignore ne contient le pattern `out/` seul                |
 | P-909    infrastructure/adapters/in/ et out/ ne sont pas ignorés           |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          gitignore-harmonizer fonctionne                                  |
 | ✓          P-908 passe                                                      |
 | ✓          P-909 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `.gitignore` de GeriCode
