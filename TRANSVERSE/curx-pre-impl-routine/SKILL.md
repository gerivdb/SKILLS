---
name: curx-pre-impl-routine
description: "Pre-implementation routine for CURX tasks: read PRD/MOC, verify benchmark, update docs, implement atomically, verify proof-of-life. Use before any CURX implementation."
triggers:
  - "implémenter CURX"
  - "CURX implementation"
  - "pre-impl CURX"
  - "routine CURX"
domain: curx
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-09-12
updated: 2026-09-12
tags:
  - curx
  - pre-impl
  - benchmark
  - kg-l
  - voltax
phi_weight: 0.010
deps:
  - pre-impl-inventory
  - slm-micro-executor
  - micro-commit-orchestrator
---

# curx-pre-impl-routine

> **IntentHash**: `0xCURX_PRE_IMPL_ROUTINE_20260912`  
> **Version**: 1.0.0  
> **Domain**: CURX  

---

## Objectif

Documenter et executer une pre-routine systemique **avant toute implementation** CURX visant a ameliorer le benchmark score.

---

## Déclencheur

Toute tache d'implementation CURX touchant :
- Les metriques benchmark (`causal_accuracy`, `fragility`, `generalization`, `counterfactual_depth`)
- Le score global CURX
- Les engines optionnelles
- Les tests d'integration

---

## Protocole obligatoire

### Étape 1 — Lire les PRD/MOC et documents de reference
```
GET C:\DevTools\CURX\PRD-CURX\*.md
GET C:\DevTools\PRD-MOC\PRD-MOC-CURX-*.md
GET C:\DevTools\CURX_IDEAS.md
GET C:\DevTools\INTENT-MAGISTRAL-CURX-DAG.md
→ Verifier que le plan d'amelioration 100% est documente
→ Si absent : STOP — completer les PRD/MOC avant implementation
```

### Étape 2 — Verifier l'etat actuel du benchmark
```powershell
cd D:\DO\WEB\TOOLS\L0-CANON\VOLTX
python scorecard.py --curx
→ Noter les scores actuels par niveau
→ Identifier les metriques < cible 100%
```

### Étape 3 — Mettre a jour les PRD/MOC avec le plan d'amelioration
- Ajouter un tableau "Plan d'Amelioration 100%" dans chaque PRD/MOC concerne
- Documenter les actions par metrique
- Mettre a jour les criteres d'acceptation

### Étape 4 — Implementer atomiquement
- Une action = un fichier = un commit
- Maximum 3 fichiers modifies entre deux commits
- Ne JAMAIS attendre plus de 30 minutes sans commit

### Étape 5 — Verifier la preuve d'execution
```powershell
python scorecard.py --curx
→ Tous les niveaux doivent afficher ✅ PASS
→ Score global ≥ 100/100
```

### Étape 6 — Mettre a jour le journal de bord
- Mettre a jour `CURX_IDEAS.md` section 15
- Commit avec IntentHash horodate

---

## Checklist avant implementation

- [ ] PRD/MOC lus et a jour avec plan 100%
- [ ] Benchmark actuel execute et scores notes
- [ ] Actions d'amelioration identifiees par metrique
- [ ] Tests existants verifies (19/19 TALEX + 22/22 KIVA-CLI)
- [ ] FLEX live confirme (`/health` = 200)
- [ ] KG-L live confirme (`/health` = 200)

---

## Anti-patterns bloquants

- Implementer sans lire les PRD/MOC d'abord
- Modifier les seuils sans documenter le plan d'amelioration
- Commit multiple sans preuve d'execution entre chaque
- Ignorer les tests existants avant modification

---

## Référence ADR

- **ADR** : ADR-2026-09-12-CURX-PRE-IMPL-ROUTINE
- **IntentHash** : `0xCURX_PRE_IMPL_ROUTINE_20260912`
- **Dépôt** : gerivdb/DevTools
- **Statut ADR** : proposed
