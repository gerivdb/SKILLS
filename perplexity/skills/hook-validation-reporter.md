---
type: skill
version: "1.0.1"
date: "2026-06-19"
intent_hash: 0xHOOK_VALIDATION_REPORTER_phi1.000
status: active
trit_primitive: TritReportHook
tags: [hooks, git, brgs, pre-push, reporting, validation]
layer: "L3_DEVTOOLS"
nexusTags: ["CONFORME_NEXUS", "HOOKS", "REPORTING"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 — gap interpretation hooks BRGS detecte session ECOS-CLI"}
  - {v: "1.0.1", date: "2026-06-19", notes: "Harmonisation intent_hash phi convention (phi vs φ unicode)"}
---

# hook-validation-reporter

## Purpose

Interprète et formate les **sorties des hooks git** (pre-push, BRGS, HITL-gate) pour les intégrer dans le rapport de passe courant. Distingue `PASS` / `WARN` / `FAIL` avec actions recommandées par niveau. Émet un résumé inline dans le rapport de session — traite la validation de hook comme un signal graduel, pas binaire.

## Trigger

Utiliser quand :
- hook pre-push déclenché avant ou pendant une passe
- résultat BRGS reçu (PASS, WARN, ou FAIL)
- hook FAIL nécessite une décision
- rapport de passe post-push à compléter
- audit post-session des validations de hooks

## Niveaux de résultat

| Niveau | Signification | Action recommandée |
|---|---|---|
| `PASS` | Toutes les règles validées | Documenter en ✅, continuer |
| `WARN` | Règle non-bloquante non satisfaite | Documenter ⚠️, décider HITL si φ-CPS impacté |
| `FAIL` | Règle bloquante non satisfaite | STOP, corriger avant de continuer |
| `SKIP` | Hook non applicable (ENV2/ENV3) | Documenter comme non-vérifié |

## Structure du rapport de hook

```
[HOOK_VALIDATION_REPORT] {timestamp}
[HOOK] Type: pre-push | BRGS | HITL-gate | post-merge
[HOOK] Branche: {nom}
[HOOK] Commit: {SHA}
[HOOK] Résultat global: PASS | WARN | FAIL | SKIP
[HOOK] Détail:
  - Règle {R1}: PASS — {description}
  - Règle {R2}: WARN — {description} → Action: {action}
  - Règle {R3}: FAIL — {description} → Correction: {correction}
[HOOK] Impact φ-CPS: AUCUN | POSSIBLE | CONFIRMÉ
[HOOK] Action finale: CONTINUER | HITL | ROLLBACK
```

## Cas réel — session ECOS-CLI 2026-06-18

```
[HOOK_VALIDATION_REPORT] 2026-06-18 21:04 CEST
[HOOK] Type: BRGS pre-push
[HOOK] Résultat global: PASS (avec 2 WARN)
[HOOK] Détail:
  - Branches supprimées: PASS — 5/5 confirmées mergées
  - intent_hash format: WARN — φ unicode vs phi ASCII non normalisé
  - Branche préfixe non-std: WARN — identifiée, à résoudre passe 10
[HOOK] Impact φ-CPS: AUCUN
[HOOK] Action finale: CONTINUER (WARNs documentés pour passe 10)
```

## Intégration dans rapport de passe

Format inline standardisé à la fin de chaque rapport de passe :

```markdown
### Validation hooks
| Hook | Résultat | Notes |
|------|----------|-------|
| BRGS pre-push | ✅ PASS | 2 WARN mineurs documentés |
| intent_hash | ⚠️ WARN | φ → phi, résolu passe N+1 |
```

## Intégration écosystème

- **Alimenté par** : `branch-lifecycle-intent-tracker` (contexte intent des branches pushées)
- **Alimente** : `adaptive-passe-sequencer` (si FAIL → rollback / si WARN → note inter-passes)
- **Déclenche** : `hitl-gate-emitter` si résultat FAIL bloquant
- **Référence** : `BRIDGES.yaml` pre_decision_checks (règles hook par strate)
