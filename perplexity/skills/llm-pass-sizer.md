---
type: skill
version: "1.0.0"
date: "2026-06-18"
intent_hash: 0xLLM_PASS_SIZER_φ1.000
status: active
trit_primitive: TritPlanDecompose
tags: [llm, pass-design, context-budget, adaptability, session-management]
layer: "L2_COGNITION"
nexusTags: ["CONFORME_NEXUS", "LLM_ADAPTIVE", "PASS_DESIGN"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 ECOS-CLI — gap adaptabilite LLM detecte session branch-cleanup"}
---

# llm-pass-sizer

## Purpose

Découpe une tâche macro en passes atomiques calibrées selon le **budget context + tool_calls** du LLM actif. Évite le context overflow silencieux et les sessions qui dérivent sans plan déclaré.

## Trigger

Utiliser quand :
- tâche implique > 3 repos gerivdb/*
- plan estimé > 5 étapes
- session prévue > 3 passes
- mention "passe N", "multi-repo", "plan itératif"
- avant toute séquence de passes numérotées

## Contexte LLM actif

| ENV | LLM | Context max | tool_calls/tour | Stratégie passes |
|---|---|---|---|---|
| ENV1 (SaaS) | Sonnet 4.6 / Perplexity | ~200k tokens | 3 | Passes larges, batch MCP agressif |
| ENV2 (Z600 local) | Owl Alpha SLM | ~4k tokens | 0 (pas MCP) | Micro-passes ≤ 200 tokens prompt |
| ENV3 (Mistral local) | Mistral 7B | ~8k tokens | 0 (pas MCP) | Passes courtes, outputs fichiers |

**Règle critique ENV1** : 3 tool_calls max par tour → toujours batch les lectures MCP (ex: lire 2 fichiers + 1 liste en un tour).

## Protocole

### Étape 1 — Identifier l'ENV et le LLM actif

```
[PASS_SIZER] ENV: ENV1 (Perplexity Sonnet 4.6)
[PASS_SIZER] Budget context: ~200k tokens
[PASS_SIZER] Budget tool_calls/tour: 3
[PASS_SIZER] Stratégie: passes larges, MCP batch
```

### Étape 2 — Décomposer la tâche macro

Pour chaque sous-objectif identifié, estimer :

```
Passe N | Objectif | Repos impliqués | Tool calls estimés | Tokens estimés | Critère succès
```

### Étape 3 — Émettre le plan de passes

```
[PASS_SIZER] Plan généré — 4 passes:
P1: Lecture état initial        | 2 repos | 2 tool_calls | ~5k tokens  | ✅ état connu
P2: Modifications branche X     | 1 repo  | 3 tool_calls | ~8k tokens  | ✅ PR créée
P3: Modifications branche Y     | 1 repo  | 3 tool_calls | ~8k tokens  | ✅ PR créée
P4: Nettoyage + rapport         | 1 repo  | 2 tool_calls | ~3k tokens  | ✅ rapport émis
```

### Étape 4 — Appliquer les règles de calibration

**Règles ENV1 (Perplexity SaaS) :**
- Max 3 tool_calls par tour → si une passe en nécessite 5, la split en 2 passes
- Batch les opérations de lecture en début de passe
- Réserver 1 tool_call pour une éventuelle correction en fin de passe
- Si une passe dépasse ~80k tokens estimés → split obligatoire

**Règles ENV2/ENV3 (SLM local) :**
- Voir skill `slm-local-prompt-design` : prompts ≤ 200 tokens
- Chaque passe = 1 fichier créé ou 1 patch appliqué
- Aucun outil MCP → toutes les opérations via shell local

### Étape 5 — Checkpoint inter-passes

À chaque fin de passe, émettre :

```
[PASS_SIZER] Passe N terminée
[PASS_SIZER] État: {résumé ≤ 100 tokens}
[PASS_SIZER] Prochain: Passe N+1 — {objectif}
[PASS_SIZER] Goto: continuer | pause HITL | rollback
```

## Exemples de découpe

### Tâche macro : "Nettoyer 5 branches + créer 2 PRs + mettre à jour NEXUS"

```
P1: Audit branches (lecture état) — 2 tool_calls
P2: Supprimer branches 1-3       — 3 tool_calls
P3: Supprimer branches 4-5 + PR1 — 3 tool_calls
P4: PR2 + update NEXUS           — 3 tool_calls
P5: Rapport final                — 1 tool_call
→ 5 passes au lieu d'un monobloc qui dépasserait le budget
```

## Intégration écosystème

- **Précède** : `adaptive-passe-sequencer` (orchestration de la séquence)
- **Complémente** : `llm-tool-budget-guard` (surveillance en cours de passe)
- **Référence** : `slm-local-prompt-design` (règles SLM si ENV2/ENV3)
- **Déclenche** : `session-snapshot` si passe > 60 min
