---
type: skill
version: "1.0.1"
date: "2026-06-19"
intent_hash: 0xADAPTIVE_PASSE_SEQUENCER_phi1.000
status: active
trit_primitive: TritSequencePasse
tags: [session-management, pass-sequencing, context, rollback, orchestration]
layer: "L2_COGNITION"
nexusTags: ["CONFORME_NEXUS", "SESSION_MANAGEMENT", "PASS_SEQUENCING"]
slotWeight: 2
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 — gap sequençage passes longues detecte session ECOS-CLI"}
  - {v: "1.0.1", date: "2026-06-19", notes: "Harmonisation intent_hash phi convention (phi vs φ unicode)"}
---

# adaptive-passe-sequencer

## Purpose

Orchestre une **séquence de passes numérotées** dans une session longue humain-LLM. Émet à chaque passe : état précédent (résumé ≤ 200 tokens), objectif courant, critères de succès, et goto suivant. Intègre un mécanisme de rollback si une passe échoue. Évite la perte de contexte sur des sessions > 1h.

## Trigger

Utiliser quand :
- session > passe 3 déjà complétée
- avant de lancer passe N (N > 2)
- contexte à risque de drift (session > 45 min)
- après un FAIL de hook ou une passe incomplète
- demande de reprise après interruption

## Structure d'une passe

```
[SEQUENCER] Passe N / {total estimé}
[SEQUENCER] État précédent (≤ 200 tokens): {résumé passe N-1}
[SEQUENCER] Objectif: {description claire}
[SEQUENCER] Repos impliqués: {liste}
[SEQUENCER] Critères de succès:
  - {critère 1}
  - {critère 2}
[SEQUENCER] Outils planifiés: {N tool_calls}
[SEQUENCER] Rollback: {action si échec}
[SEQUENCER] Goto si succès: Passe N+1 | FIN | HITL
```

## Protocole de checkpoint inter-passes

### Fin de passe réussie

```
[SEQUENCER] ✅ Passe N terminée
[SEQUENCER] Livrable: {commit SHA | fichier | PR #N}
[SEQUENCER] État résumé: {≤ 100 tokens}
[SEQUENCER] Prochain: Passe N+1 — {objectif}
```

### Fin de passe avec WARN

```
[SEQUENCER] ⚠️ Passe N terminée avec WARN
[SEQUENCER] WARN: {description}
[SEQUENCER] Décision: CONTINUER (WARN documenté) | HITL requis
[SEQUENCER] WARN reporté: noter dans backlog passe N+1
```

### Fin de passe avec FAIL

```
[SEQUENCER] ❌ Passe N FAIL
[SEQUENCER] Cause: {description}
[SEQUENCER] Rollback: {action}
[SEQUENCER] Décision: RETRY | HITL | ABANDON
```

## Gestion de la dérive de contexte

Si session > 45 min sans checkpoint :

```
[SEQUENCER] CONTEXT_DRIFT_RISK détecté
[SEQUENCER] Dernière passe confirmée: Passe {N} ({timestamp})
[SEQUENCER] Actions en vol: {liste}
[SEQUENCER] Recommandation: émettre état résumé maintenant
```

## Exemple — session ECOS-CLI 2026-06-18

```
Session: 9 passes (LORE analyse + branches cleanup + skills creation)
Durée estimée: > 2h
Dérive détectée: non (checkpoints émis à chaque passe)
WARN accumulés: 2 (intent_hash format + branche non-std)
Statut: 9/9 passes terminées, 2 WARN reportés passe 10
```

Ce skill aurait formalisé le plan de 9 passes en début de session et émis des checkpoints structurés.

## Chaîne d'orchestration

```
llm-pass-sizer  →  adaptive-passe-sequencer  →  llm-tool-budget-guard
      ↓                      ↓                          ↓
  Plan passes          Checkpoint inter-passes      Budget par tour
      ↓                      ↓
hitl-gate-emitter    hook-validation-reporter
  (si FAIL)             (résultat hooks)
```

## Intégration écosystème

- **Précédé par** : `llm-pass-sizer` (plan de passes)
- **Alimente** : `hook-validation-reporter` (état hooks entre passes)
- **Utilise** : `contextual-stash-manager` (état inter-passes si > 2k tokens)
- **Déclenche** : `hitl-gate-emitter` (si FAIL non récupérable)
- **Référence** : `adaptive-passe-sequencer` est le nœud central — toutes les passes longues passent par lui
