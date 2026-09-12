---
name: session-workflow-closer
description: "End-of-session workflow: verify no orphan branches, ensure all feat branches have PRs or are merged, clean up local branches, and confirm no direct main push occurred. Use at session end."
triggers:
  - "fin de session"
  - "session end"
  - "cloture session"
  - "cleanup branches"
  - "verifier branches"
domain: transverse
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-09-12
updated: 2026-09-12
tags:
  - git
  - session
  - cleanup
  - branch
  - pr
  - workflow
phi_weight: 0.008
deps:
  - branch-lifecycle
  - pr-review-resolver
  - git-workflow-guardian
---

# session-workflow-closer

> **IntentHash**: `0xSESSION_WORKFLOW_CLOSER_20260912`  
> **Version**: 1.0.0  
> **Domain**: transverse  

---

## Objectif

Verifier en fin de session que :
1. Aucune branche orpheline non mergee
2. Toutes les branches feat ont une PR ou sont mergees
3. Aucun commit direct sur `main` sans PR
4. Les branches locales sont nettoyees

---

## Protocole obligatoire

### Étape 1 — Lister les branches locales
```powershell
git branch --merged main
git branch --no-merged main
```
→ Si branches feature non mergees → continuer Étape 2  
→ Si aucune branche feature → passer à Étape 5

### Étape 2 — Vérifier la cohérence avec la SOT
```powershell
git log main..feature-branch --oneline
```
→ Si la branche a des commits uniques → continuer Étape 3  
→ Si la branche est déjà couverte par main → passer à Étape 5

### Étape 3 — Vérifier la présence d'une PR
```powershell
# Via KIVA-CLI ou ECOS-CLI
python -m kiva.cli pr list --head <branche>
```
→ Si PR existe → continuer Étape 4  
→ Si pas de PR → **STOP**, demander création de PR

### Étape 4 — Merger via KIVA-CLI / ECOS-CLI
```powershell
# Option A: KIVA-CLI
python -m kiva.cli merge feature-branch

# Option B: ECOS-CLI
python -m ecos.cli merge feature-branch
```
→ Si succes → continuer Étape 5  
→ Si echec (conflits) → signaler, arreter

### Étape 5 — Nettoyer les branches locales
```powershell
git branch --merged main | grep -v "main" | xargs git branch -d
```
→ Supprime les branches locales deja mergees

### Étape 6 — Vérifier qu'aucun commit direct sur main n'a été pushé
```powershell
git log origin/main..main --oneline
```
→ Si commits locaux sur main non présents sur origin/main → **STOP**, demander création de PR

---

## Anti-patterns bloquants

- Laisser une branche feature vivante apres merge
- Supprimer une branche distante sans avoir merge la PR
- Ignorer les branches en attente a la fin d'une session
- Push direct sur `main` sans PR

---

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
