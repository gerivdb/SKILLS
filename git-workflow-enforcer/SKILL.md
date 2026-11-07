---
type: SKILL
version: "1.0.0"
intent_hash: 0xGIT_WORKFLOW_ENFORCER_20260808
---

# Git Workflow Enforcer

## Objectif

Bloquer tout travail sur `main` sans branche `feat/<slug>` dédiée.

## Déclencheur

Avant tout commit, push, ou modification de fichier dans un repo git.

## Règles

### 1. Vérifier la branche courante

```powershell
git branch --show-current
```

→ Si `main` → **STOP** : INTERDIT de travailler sur main
→ Si `feat/*`, `fix/*`, `chore/*`, `ops/*`, `hotfix/*`, `release/*` → continuer

### 2. Vérifier la création de la branche

```powershell
git log --oneline -5
```

→ Si pas de commit sur branche feat → vérifier création

### 3. Vérifier le mapping IntentHash

```powershell
# Vérifier que le message de commit contient l'IntentHash
git log -1 --format=%B
```

→ Si pas d'IntentHash → **STOP** : rejeter commit

### 4. Vérifier l atomicité

```powershell
git diff --cached --name-only | Measure-Object | Select-Object -ExpandProperty Count
```

→ Si > 3 fichiers → **STOP** : commit trop volumineux

## Anti-patterns bloquants

- Commit sur `main` → BLOCKING
- Commit sans IntentHash → BLOCKING
- Commit avec > 3 fichiers → BLOCKING
- Push sans remote safety → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENTIC-GIT-WORKFLOW
- **IntentHash** : 0xAGENTIC_GIT_WORKFLOW_20260808
- **Statut ADR** : proposed
