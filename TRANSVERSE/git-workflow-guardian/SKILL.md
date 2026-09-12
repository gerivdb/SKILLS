---
name: git-workflow-guardian
description: "Enforce correct git workflow: never push main directly, use feature branches + PR, respect repo-specific branch taxonomy and ALFRED/BRGS guards. Use before any git push or branch creation."
triggers:
  - "git push"
  - "push commits"
  - "create branch"
  - "feature branch"
  - "PR workflow"
  - "ne pas push sur main"
  - "workflow git"
domain: transverse
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-09-12
updated: 2026-09-12
tags:
  - git
  - workflow
  - pr
  - branch
  - alfred
  - brgs
  - devtools
phi_weight: 0.010
deps:
  - branch-guard
  - branch-taxonomy-enforcer
  - pre-push-path-audit
---

# git-workflow-guardian

> **IntentHash**: `0xGIT_WORKFLOW_GUARDIAN_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  
> **Scope**: tous les repos `D:\DO\WEB\TOOLS\*` et `C:\DevTools`

---

## Objectif

Verrouiller le workflow git pour **ne plus jamais** :
- pusher directement sur `main`
- créer une branche sans préfixe autorisé
- ignorer les guards locaux (`ALFRED`, `BRGS`)
- oublier la logique `feat -> push -> PR -> merge`

---

## Protocole obligatoire

### Avant tout `git push`

1. Lire `git branch --show-current`
2. Si branche = `main` → **STOP**, créer d'abord une branche de feature
3. Vérifier le préfixe de branche via `branch-taxonomy-enforcer`
4. Vérifier les chemins modifiés via `pre-push-path-audit`
5. Si tous les checks passent → `git push origin <branche>`
6. Créer la PR via KIVA-CLI / ECOS-CLI (interdiction `gh pr` en BDCP)

### Logique feature branch correcte

```powershell
# 1. Rester sur main a jour
git checkout main
git pull origin main

# 2. Creer une branche de feature
git checkout -b feat/<slug>-<id>

# 3. Committer les changements
git add <fichiers>
git commit -m "feat(<scope>): <desc>"

# 4. Pousser la branche
git push origin feat/<slug>-<id>

# 5. Creer la PR via KIVA-CLI
python -m kiva.cli pr create --title "..." --body "..."
```

### En cas de commits déjà sur main (comme aujourd'hui)

1. **Ne pas push** : `git push origin main` est interdit par ALFRED
2. **Créer une branche depuis main** : `git checkout -b feat/<slug>-<id>`
3. **Reset main** sur `origin/main` : `git checkout main && git reset --hard origin/main`
4. **Re-appliquer les changements** sur la branche feat
5. **Pousser la branche** et créer la PR

---

## Guards transversaux

| Guard | Action |
|-------|--------|
| **ALFRED** | Bloque le push direct sur `main` → utiliser une branche feat |
| **BRGS** | Vérifie le préfixe de branche → utiliser `feat/`, `fix/`, `docs/`, `chore/`, `refactor/` |
| **Taxonomie unifiée** | Format `type/jurisdiction-slug-id` → ex: `feat/env2-lxc-network-001` |
| **BDCP** | Interdit `gh pr` → utiliser KIVA-CLI / ECOS-CLI uniquement |

---

## Anti-patterns bloquants

- `git push origin main` → **INTERDIT** (ALFRED BLOCK)
- Créer une branche `docs/curx-...` en contournement → **INTERDIT** (taxonomie non conforme)
- Commiter sur `main` puis push → **INTERDIT** (workflow inverse)
- Utiliser `gh pr create` → **INTERDIT** (BDCP)
- Ignorer les guards locaux → **INTERDIT**

---

## Checklist avant push

- [ ] Branche actuelle ≠ `main` ?
- [ ] Préfixe de branche autorisé (`feat/`, `fix/`, `docs/`, `chore/`, `refactor/`) ?
- [ ] Format taxonomie respecté (`type/jurisdiction-slug-id`) ?
- [ ] `pre-push-path-audit` passé ?
- [ ] PR créée via KIVA-CLI / ECOS-CLI (pas `gh`) ?

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
