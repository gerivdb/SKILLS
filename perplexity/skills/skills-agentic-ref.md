---
name: skills-agentic-ref
version: "1.0.0"
description: "Référence vers le pipeline SKILLS_AGENTIC v2 — 9 agents (DELEGATOR, PARSER, REWRITER, PLANNER, ROUTER, COVERAGE+DRAFT+GAP, FANOUT, SYNTH, ITERATOR). 8 patterns Google RAG exploités. Utiliser quand l'utilisateur mentionne 'pipeline agentic', 'SKILLS_AGENTIC', 'orchestrer skills', 'DELEGATOR', 'REWRITER', 'DRAFT agent', 'GAP analyzer'."
triggers:
  - "pipeline agentic"
  - "SKILLS_AGENTIC"
  - "orchestrer skills"
  - "DELEGATOR"
  - "REWRITER"
  - "DRAFT agent"
  - "GAP analyzer"
  - "COVERAGE agent"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "perplexity/skills/skills-agentic.md v2"
  - "perplexity/skills/skills-coverage.md v2"
  - "perplexity/skills/skills-router.md v1"
  - "perplexity/skills/skills-rewriter.md v1"
  - "perplexity/skills/skills-agentic-test.md v2"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — référence SKILLS_AGENTIC v2"}
trit_primitive: TritDocumentClassify
---

# SKILLS-AGENTIC-REF — Référence du pipeline agentic v2

## Domaine et périmètre

Ce skill est la **référence centralisée** pour le pipeline SKILLS_AGENTIC v2. Il pointe vers les 5 fichiers skills qui composent le pipeline et documente l'architecture 9 agents.

## Architecture 9 agents

```
Requête → DELEGATOR (évalue complexité → niveau 1/2/3)
              │
              ▼ (niveau 2 ou 3)
          PARSER (décompose en intents)
              │
              ▼
          REWRITER (reformule en sous-quêtes atomiques)
              │
              ▼
          PLANNER (sélectionne les skills)
              │
              ▼
          ROUTER (mappe skill → repo cible)
              │
              ▼
          COVERAGE (vérifie couverture + DRAFT + GAP ANALYZER)
              │
              ▼ (si SUFFICIENT)
          FANOUT (exécute en parallèle)
              │
              ▼
          SYNTH (agrège les résultats)
              │
              ▼
          Réponse finale

          (si INSUFFICIENT → ITERATOR relance REWRITER + PLANNER avec feedback ciblé)
```

## Fichiers skills

| Fichier | Agent(s) | Rôle |
|---------|----------|------|
| `skills-agentic.md` | DELEGATOR, PARSER, PLANNER, FANOUT, SYNTH, ITERATOR | Orchestrateur principal |
| `skills-coverage.md` | COVERAGE, DRAFT, GAP ANALYZER | Vérificateur de couverture |
| `skills-router.md` | ROUTER | Routing cross-repo |
| `skills-rewriter.md` | REWRITER | Reformulation des intents |
| `skills-agentic-test.md` | TEST | Suite de tests |

## 8 patterns Google RAG exploités

| # | Pattern Google | Adaptation gerivdb |
|---|----------------|--------------------|
| 1 | Sufficient Context Agent | COVERAGE Agent (4 critères) |
| 2 | Cross-Corpus Retrieval | ROUTER Agent (185 repos) |
| 3 | Search Fanout + Iteration | FANOUT + ITERATOR |
| 4 | Query Rewriter | REWRITER Agent |
| 5 | Intermediate Draft | DRAFT AGENT |
| 6 | Missing Pieces Analysis | GAP ANALYZER |
| 7 | Orchestrator conditionnel | DELEGATOR (3 niveaux) |
| 8 | Synthesis Agent | SYNTH Agent |

## Niveaux de délégation

| Niveau | Complexité | Agents activés | Latence |
|--------|------------|----------------|---------|
| 1 — Simple | 1 intent, 1 strate | Skill direct | < 2s |
| 2 — Moyen | 2-3 intents, 1-2 strates | Pipeline court (6 agents) | < 8s |
| 3 — Complexe | 4+ intents, cross-strate | Pipeline complet (9 agents) | < 15s |

## Intégration

- **Dépôts** : SKILLS (tous les skills agentic)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : uae-keel-coords (routing UAE), keel-peg-parser (parsing KEEL)
