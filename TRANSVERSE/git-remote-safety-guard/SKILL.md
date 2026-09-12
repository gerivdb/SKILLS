---
name: git-remote-safety-guard
description: "Verify git remote safety before push: correct remote URL, correct branch, no force push without verification. Use before any git push operation."
triggers:
  - "git push"
  - "remote safety"
  - "verifier remote"
  - "securite push"
domain: transverse
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-09-12
updated: 2026-09-12
tags:
  - git
  - push
  - remote
  - safety
  - alfred
  - brgs
phi_weight: 0.008
deps:
  - branch-guard
  - git-workflow-guardian
  - pre-push-path-audit
---

# git-remote-safety-guard

> **IntentHash**: `0xGIT_REMOTE_SAFETY_GUARD_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  

---

## Objectif

Verifier avant tout `git push` que :
1. Le remote est correct
2. La branche est correcte
3. Aucun force push non intentionnel
4. L'historique distant n'est pas ecrase

---

## Protocole obligatoire

### Étape 1 — Vérifier le remote
```powershell
git remote -v
```
→ Vérifier que le remote correspond au repo attendu  
→ Si mismatch → `git remote set-url origin <url_correcte>`

### Étape 2 — Vérifier la branche
```powershell
git branch --show-current
```
→ Si HEAD détaché → `git checkout -B main HEAD`  
→ Si branche = `main` → **STOP**, utiliser une branche feat

### Étape 3 — Vérifier l'historique distant
```powershell
git log origin/<branche> --oneline -5
```
→ Vérifier que le distant n'a pas été écrasé  
→ Si historique incompatibe → **STOP**, demander confirmation

### Étape 4 — Push SANS force
```powershell
git push origin <branche>
```
→ Ne JAMAIS utiliser `--force` sans avoir vérifié les étapes 1-3

### Étape 5 — En cas de force push
```powershell
# UNIQUEMENT si les étapes 1-3 sont OK ET si c'est intentionnel
git push --force origin <commit_sha>:<branche>
```
→ Vérifier le résultat avec `gh api repos/<owner>/<repo>/git/refs/heads/<branche>`

---

## Anti-patterns bloquants

- `git push --force` sans vérifier `git remote -v`
- `git push` sans vérifier `git branch`
- Changer de repo sans utiliser `workdir` ou des chemins absolus
- Push depuis `main` sans branche feat

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
