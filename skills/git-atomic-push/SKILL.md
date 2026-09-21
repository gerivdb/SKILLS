---
type: skill
version: "1.0.0"
date: "2026-09-15"
status: draft
intent_hash: 0xGIT_ATOMIC_PUSH_20260915
extends: git-remote-safety-guard
---

# Skill: git-atomic-push

## Purpose
Effectue des commits atomiques et des pushes sécurisés, conformes aux règles KiloCode :
- Maximum 3 fichiers modifiés par commit
- Vérification du remote avant push
- Pas de force push sans vérification
- Validation des tests avant commit

## Context
Ce skill est utilisé à la fin de chaque session KiloCode ou quand un drift est détecté.
Il remplace les commandes git manuelles par un workflow sécurisé et traçable.

## Prerequisites
- Git configuré avec remote correct
- Tests passants (`cargo test` / `pytest`)
- Aucun secret dans les fichiers modifiés

## Workflow

### 1. Vérification de l'état
```powershell
git status --short
git diff --stat
```

### 2. Vérification du remote
```powershell
git remote -v
git branch
```

### 3. Vérification des tests
```powershell
# Rust
cargo test

# Python
pytest <repo>/tests/ -v
```

### 4. Commit atomique (max 3 fichiers)
```powershell
git add <file1> <file2> <file3>
git commit -m "feat(scope): description atomique"
```

### 5. Push sécurisé
```powershell
git push origin <branch>
```

## Anti-patterns
- ❌ `git add -A` avec plus de 3 fichiers
- ❌ `git push --force` sans vérification
- ❌ Commit avec message vague ("WIP", "updates")
- ❌ Push sans vérifier les tests

## References
- **Rule** : git-atomic-commit.md
- **Rule** : git-remote-safety.md
- **ADR** : ADR-099-git-atomic-commit
- **ADR** : ADR-094-git-remote-safety-protocol
