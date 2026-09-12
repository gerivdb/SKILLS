---
name: pre-push-path-audit
description: "Audit paths before git push: verify local_path ↔ remote full_name consistency, detect untracked cross-repo files, and ensure no forbidden paths are pushed. Use before any git push."
triggers:
  - "git push"
  - "pre-push audit"
  - "audit chemins"
  - "verifier chemins"
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
  - audit
  - path
  - cross-repo
phi_weight: 0.008
deps:
  - branch-guard
  - git-workflow-guardian
---

# pre-push-path-audit

> **IntentHash**: `0xPRE_PUSH_PATH_AUDIT_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  

---

## Objectif

Verifier avant tout `git push` que :
1. Le remote correspond au repo attendu
2. Les chemins modifies sont autorises
3. Aucun fichier cross-repo non autorise n'est inclus
4. La branche correspond bien au repo

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

### Étape 3 — Vérifier les chemins modifies
```powershell
git status --short
git diff --cached --name-only
```
→ Vérifier que les fichiers modifiés sont autorises  
→ Si fichiers hors périmètre → **STOP**, demander confirmation

### Étape 4 — Vérifier la cohérence local_path ↔ full_name
```powershell
# Lire known_repositories.yaml
# Vérifier que local_path correspond à full_name
```
→ Si mismatch → **STOP**, corriger avant de continuer

### Étape 5 — Vérifier les fichiers non suivis cross-repo
```powershell
# Vérifier les fichiers non suivis dans D:\DO\WEB\TOOLS\*
# Si fichiers présents dans un repo mais appartenant à un autre → **STOP**
```

---

## Anti-patterns bloquants

- Push sans vérifier `git remote -v`
- Push depuis `main` sans branche feat
- Inclure des fichiers cross-repo non autorises
- Ignorer les fichiers non suivis massifs

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
