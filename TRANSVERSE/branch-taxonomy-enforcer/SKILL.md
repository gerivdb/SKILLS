---
name: branch-taxonomy-enforcer
description: "Enforce repo-specific branch naming taxonomy. Use before creating any git branch to ensure prefix and slug format are valid for the target repo."
triggers:
  - "create branch"
  - "git checkout -b"
  - "branch naming"
  - "taxonomie branche"
  - "préfixe branche"
domain: transverse
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-09-12
updated: 2026-09-12
tags:
  - git
  - branch
  - taxonomy
  - naming
  - alfred
  - brgs
phi_weight: 0.008
deps:
  - branch-guard
---

# branch-taxonomy-enforcer

> **IntentHash**: `0xBRANCH_TAXONOMY_ENFORCER_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  

---

## Objectif

Verrouiller le nommage des branches pour respecter :
- Les préfixes autorisés par repo
- Le format unifié `type/jurisdiction-slug-id`
- Les guards `ALFRED` et `BRGS`

---

## Taxonomie par repo

| Repo | Préfixes autorisés | Format attendu |
|------|-------------------|----------------|
| **DevTools** | `devtools/`, `fix/`, `chore/`, `docs/`, `refactor/` | `type/jurisdiction-slug-id` |
| **VOLTX** | `feat/`, `fix/`, `chore/`, `docs/`, `refactor/` | `type/slug-id` |
| **KG-L** | `fix/`, `docs/`, `chore/`, `refactor/` | `type/slug-id` |
| **TALEX** | `feat/`, `fix/`, `chore/`, `docs/`, `refactor/` | `type/slug-id` |
| **FLEX** | `feat/`, `fix/`, `chore/`, `docs/`, `refactor/` | `type/slug-id` |
| **KIVA-CLI** | `feat/`, `fix/`, `chore/`, `docs/`, `refactor/` | `type/slug-id` |

---

## Règles

### 1. Vérifier le repo courant
```powershell
git remote -v
git rev-parse --show-toplevel
```

### 2. Lister les préfixes autorisés
- Lire `.githooks/alfred.ps1` ou `BRGS` config du repo
- Si préfixe non autorisé → **STOP**, demander confirmation

### 3. Valider le format
- Format attendu : `type/jurisdiction-slug-id`
- Exemple valide : `feat/env2-lxc-network-001`
- Exemple invalide : `curx-100pct-benchmark-20260912` (pas de préfixe)

### 4. En cas de non-conformité
- **STOP** : ne pas créer la branche
- Proposer un nom conforme
- Si validation explicite → continuer avec `--no-verify`

---

## Anti-patterns bloquants

- Créer une branche sans préfixe autorisé
- Utiliser un nom libre (`curx-100pct-...`) sans préfixe
- Ignorer les guards `ALFRED` / `BRGS`
- Forcer le push avec `--no-verify` sans raison valide

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
