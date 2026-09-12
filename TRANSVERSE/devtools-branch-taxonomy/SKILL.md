---
name: devtools-branch-taxonomy
description: "Enforce DevTools-specific branch naming: authorized prefixes and unified taxonomy format. Use when creating branches in C:\\DevTools."
triggers:
  - "create branch devtools"
  - "devtools branch"
  - "branche devtools"
  - "taxonomie devtools"
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
  - devtools
  - taxonomy
  - alfred
  - brgs
phi_weight: 0.008
deps:
  - branch-taxonomy-enforcer
---

# devtools-branch-taxonomy

> **IntentHash**: `0xDEVTOOLS_BRANCH_TAXONOMY_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  

---

## Objectif

Verrouiller le nommage des branches dans `C:\DevTools` selon :
- Les préfixes autorisés par `ALFRED` / `BRGS`
- Le format unifié `type/jurisdiction-slug-id`

---

## Préfixes autorisés (DevTools)

| Préfixe | Usage |
|---------|-------|
| `devtools/` | Développement DevTools spécifique |
| `fix/` | Correction de bug |
| `chore/` | Maintenance, dépendances |
| `docs/` | Documentation |
| `refactor/` | Refactorisation |

**Interdits** : `feat/`, `feature/`, `hotfix/`, `release/`, noms libres (`curx-100pct-...`)

---

## Format attendu

```
type/jurisdiction-slug-id
```

**Exemples valides** :
- `docs/curx-benchmark-100pct-20260912`
- `fix/alfred-prefix-enforcement-20260912`
- `chore/update-dependencies-20260912`

**Exemples invalides** :
- `curx-100pct-benchmark-20260912` (pas de préfixe)
- `feat/curx-100pct` (préfixe `feat/` interdit)
- `docs_curx_benchmark` (tireau lieu de slash)

---

## Protocole

### Avant toute création de branche

1. Vérifier le préfixe : doit être dans la liste autorisée
2. Vérifier le format : `type/jurisdiction-slug-id`
3. Si non-conforme → **STOP**, proposer un nom conforme
4. Si validation explicite → continuer avec `--no-verify`

### En cas de non-conformité

```powershell
# Branche créée par erreur avec mauvais nom
git branch -m <ancien_nom> <nouveau_nom_conforme>

# Si déjà poussée
git push origin --delete <ancien_nom>
git push origin <nouveau_nom>
```

---

## Guards

| Guard | Action |
|-------|--------|
| **ALFRED** | Bloque le push si préfixe non autorisé |
| **BRGS** | Vérifie le format taxonomie |
| **BDCP** | Interdit `gh pr` → utiliser KIVA-CLI |

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
