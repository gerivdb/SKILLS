---
type: skill
version: "1.0.1"
date: "2026-06-18"
intent_hash: 0xADAPTIVE_PASSE_SEQUENCER_φ1.000
status: active
trit_primitive: TritSequencePasse
tags: [passe, sequencing, adaptive, session-management, l2-cognition]
layer: "L2_COGNITION"
nexusTags: ["CONFORME_NEXUS", "SESSION_MANAGEMENT", "ADAPTIVE_SEQUENCING"]
slotWeight: 2
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 clôture axe C — gap séquençage adaptatif des passes selon contexte et budget"}
  - {v: "1.0.1", date: "2026-06-18", notes: "passe 10 — intent_hash φ1.000 validé conforme φ[X.XXX]"}
---

# adaptive-passe-sequencer

## Purpose

Orchestre le **séquençage dynamique des passes LLM** au sein d'une session de travail. Détermine l'ordre optimal des passes selon : le budget tool_calls restant, la taille du contexte accumulé, les dépendances entre tâches, et les signaux de la TRIADE (IRIS/KRONOS/FLUX). Permet de réordonner, reporter ou fusionner des passes pour maximiser la densité utile par session.

## Trigger

Utiliser quand :
- une session contient ≥ 3 passes planifiées
- une passe prend plus longtemps que prévu et menace le budget
- une tâche imprévue arrive en milieu de session
- le contexte dépasse 50% de la fenêtre disponible
- la question "dans quel ordre traiter X, Y, Z ?" se pose
- une passe échoue et des passes suivantes en dépendent

## Modèle de passe

Chaque passe est décrite par :

```yaml
passe:
  id: "P{N}"
  label: "{description courte}"
  intent: "{objectif mesurable}"
  deps: ["{P_precédente}"]
  budget_tools: {N}         # tool_calls estimés
  budget_tokens: {N}        # tokens contexte estimés
  priority: {1-5}           # 1=critique, 5=optionnel
  status: {pending|active|done|skipped|failed}
  layer: "{L0-L9}"          # strate NEXUS concernée
```

## Algorithme de séquençage

### Phase 1 — Inventaire

```
[SEQUENCER] Session: {id}
[SEQUENCER] Passes planifiées: {N}
[SEQUENCER] Budget total estimé: {T} tool_calls | {C} tokens
[SEQUENCER] Budget restant: {R} tool_calls | fenêtre {F}% pleine
```

### Phase 2 — Graphe de dépendances

```
Construction DAG: passes comme noeuds, dépendances comme arêtes
Calcul du chemin critique: séquence de passes qui détermine la durée minimale
Identification des passes parallélisables: sans dépendance mutuelle
```

### Phase 3 — Stratégie adaptative

| Situation | Stratégie |
|---|---|
| Budget confortable (> 60% restant) | Exécuter selon chemin critique + passes optionnelles |
| Budget serré (40-60% restant) | Exécuter chemin critique uniquement, reporter P4-P5 |
| Budget critique (< 40% restant) | Fusionner passes compatibles, éliminer P5 |
| Contexte > 70% plein | Déclencher `contextual-stash-manager` avant passe suivante |
| Passe échouée avec deps | Proposer chemin alternatif ou reporter la chaîne |
| Tâche imprévue haute priorité | Insérer en tête, repousser passes P4-P5 |

### Phase 4 — Émission du plan

```
[SEQUENCER] PLAN ADAPTATIF
  P{N} -> {label}           [budget: {T}t/{C}k] [priorité: {P}] [status: {s}]
  P{N} -> {label}           [budget: {T}t/{C}k] [priorité: {P}] [status: {s}]
  ...
[SEQUENCER] Chemin critique: P{a} -> P{b} -> P{c}
[SEQUENCER] Passes reportées: {liste} -> session N+1
[SEQUENCER] Passes fusionnées: {P_a + P_b -> P_ab}
[SEQUENCER] Prochain appel: {skill ou outil recommandé pour passe suivante}
```

## Application session 2026-06-18

Séquençage réel de la passe 9 :

```
[SEQUENCER] Session: 2026-06-18-ECOS-CLI-PASSE9
[SEQUENCER] Passes planifiées: 9 skills en 3 groupes

Groupe A (L2) — llm-pass-sizer + llm-tool-budget-guard
  P1 -> llm-pass-sizer            [2t/800k] [P1] done
  P2 -> llm-tool-budget-guard     [2t/900k] [P1] done
  -> push batch: 1 appel mcp_github

Groupe B (L3-CTULU) — ctulu-tool-selector + ctulu-result-integrator
  P3 -> ctulu-tool-selector       [1t/1200k][P2] done
  P4 -> ctulu-result-integrator   [1t/1100k][P2] done
  -> push batch: 1 appel mcp_github

Groupe C (L3-axe C) — branch-lifecycle + hook-validation + adaptive-sequencer
  P5 -> branch-lifecycle-intent-tracker  [1t/900k] [P3] done
  P6 -> hook-validation-reporter         [1t/1000k][P3] done
  P7 -> adaptive-passe-sequencer         [1t/1100k][P3] done (ce skill)
  -> push batch: 1 appel mcp_github

[SEQUENCER] Chemin critique: Groupe A -> B -> C (séquentiel, sans parallélisme ENV1)
[SEQUENCER] Budget consommé: ~9 tool_calls sur session
[SEQUENCER] Passes reportées: aucune — 9/9 complétées
```

## Signaux TRIADE intégrés

| Signal | Source | Impact séquençage |
|---|---|---|
| Urgence HITL | KRONOS | Insérer HITL avant passe en cours |
| Nouveau signal entrant | IRIS | Évaluer priorité vs chemin critique |
| Flux de données arrivant | FLUX | Déclencher passe data si dépendance résolue |
| Fenêtre HITL fermée (16h-07h30) | KRONOS | Pas d'attente HITL, continuer en autonome |

## Métrique de performance

```
Efficacité session = passes_complétées / passes_planifiées
Densité utile = valeur_livrée / tool_calls_consommés
Taux de report = passes_reportées / passes_totales

Cible: efficacité >= 0.85 | densité >= 0.7 | taux_report <= 0.2
```

## Intégration écosystème

- **Orchestré par** : `LLM_BOOT_PROTOCOL.md` (GATE-3 planification des passes)
- **Alimenté par** : `llm-pass-sizer` (taille des passes), `llm-tool-budget-guard` (budget)
- **Déclenche** : `contextual-stash-manager` (si contexte > 70%), `hook-validation-reporter` (fin de passe)
- **Signaux entrants** : `triade-iris`, `triade-kronos`, `triade-flux`
- **Stash des plans** : `gerivdb/NEXUS` (plans de session persistés si multi-jours)
