---
name: skills-agentic-test
version: "1.0.0"
description: "Suite de tests pour valider le pipeline SKILLS_AGENTIC. Contient 20 requêtes de test couvrant les cas nominaux, multi-intents, complexes cross-strate, edge cases, et non-régression. Utiliser quand l'utilisateur mentionne 'test agentic', 'valider pipeline', 'SKILLS_AGENTIC test', 'couverture test'."
triggers:
  - "test agentic"
  - "valider pipeline"
  - "SKILLS_AGENTIC test"
  - "couverture test"
  - "test coverage"
  - "test multi-skill"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "skills-agentic.md (orchestrateur)"
  - "skills-coverage.md (vérificateur)"
  - "skills-router.md (routeur)"
  - "MANIFEST.json (SKILLS)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — 20 requêtes de test"}
---

# SKILLS_AGENTIC_TEST — Suite de Tests

## Domaine et périmètre

Ce skill contient la **suite de tests complète** pour valider le pipeline SKILLS_AGENTIC. Il définit 20 requêtes de test couvrant tous les cas d'usage et les edge cases, avec les résultats attendus pour chaque.

## Jeu de 20 Requêtes de Test

### Catégorie A — Mono-intent (5 requêtes)

| # | Requête | Skills attendus | Verdict attendu |
|---|---------|-----------------|-----------------|
| A1 | "Vérifie la conformité NEXUS du repo FLUENCE" | nexus-auditor, reposcope-run | SUFFICIENT |
| A2 | "Génère un PRD pour la fonctionnalité X" | prd-factory | SUFFICIENT |
| A3 | "Scanne les emojis dans DevTools" | (skill existant) | SUFFICIENT |
| A4 | "Vérifie les hooks git dans ECOYSTEM" | (skill existant) | SUFFICIENT |
| A5 | "Analyse l'architecture de BRAIN" | reposcope-run | SUFFICIENT |

### Catégorie B — Multi-intents (5 requêtes)

| # | Requête | Skills attendus | Verdict attendu |
|---|---------|-----------------|-----------------|
| B1 | "Audit FLUENCE + vérifie conformité NEXUS" | reposcope-run, nexus-auditor | SUFFICIENT |
| B2 | "Crée PRD + vérifie OKR consistency" | prd-factory, nexus-core | SUFFICIENT |
| B3 | "Scanne emojis + génère rapport + corrige" | (skills existants) | SUFFICIENT |
| B4 | "Audit BRAIN + vérifie ADR + génère PRD" | reposcope-run, adr-manager, prd-factory | SUFFICIENT |
| B5 | "Vérifie structure + conformité + hooks" | reposcope-run, nexus-auditor, (hooks) | SUFFICIENT |

### Catégorie C — Complexes cross-strate (5 requêtes)

| # | Requête | Skills attendus | Verdict attendu |
|---|---------|-----------------|-----------------|
| C1 | "Audit complet FLUENCE : structure, conformité NEXUS, ADR, PRD, rapport" | reposcope-run, nexus-auditor, adr-manager, prd-factory, workflow-orchestration | SUFFICIENT |
| C2 | "Migration repo X : scan, plan, exécute, vérifie" | reposcope-run, nexus-reformer, (migration) | SUFFICIENT |
| C3 | "Gouvernance globale : NEXUS, ONTOLOGY, BRAIN, FLUENCE" | nexus-core, (ontology), reposcope-run | SUFFICIENT |
| C4 | "Refactoring cross-repo : analyse, plan, exécute, valide" | reposcope-run, nexus-reformer, skill-tester | SUFFICIENT |
| C5 | "Conformité totale : structure, ADR, PRD, OKR, hooks, emojis" | Tous les skills de conformité | SUFFICIENT |

### Catégorie D — Edge cases (3 requêtes)

| # | Requête | Comportement attendu |
|---|---------|---------------------|
| D1 | "Fais quelque chose avec le repo X" | PARSER détecte l'ambiguïté → demande clarification |
| D2 | "Audit repo INEXISTANT" | ROUTER détecte l'erreur → feedback |
| D3 | "Vérifie conformité puis ignore la conformité" | COVERAGE détecte la contradiction → feedback |

### Catégorie E — Non-régression (2 requêtes)

| # | Requête | Vérification |
|---|---------|--------------|
| E1 | "Teste le skill pruning-explainer" | Le skill existant s'active normalement |
| E2 | "Génère un diagramme Mermaid" | Le skill diagram-mermaid s'active normalement |

## Critères d'acceptation des tests

1. **20/20 requêtes** produisent les résultats attendus
2. **COVERAGE Agent** détecte 100% des gaps injectés
3. **Itération** : le pipeline converge en ≤3 itérations pour toutes les requêtes
4. **Non-régression** : les 59 skills existants continuent de fonctionner
5. **Traçabilité** : chaque test produit un log complet

## Format de sortie des tests

```markdown
## SKILLS_AGENTIC_TEST — Rapport

### Résumé
- Total : 20
- Pass : [N]
- Fail : [N]
- Coverage : [N]%

### Détails
| # | Catégorie | Requête | Verdict | Itérations | Statut |
|---|-----------|---------|---------|------------|--------|
| A1 | Mono-intent | ... | SUFFICIENT | 1 | ✅ |
| ... | ... | ... | ... | ... | ... |

### Gaps détectés
[Liste des gaps par requête]

### Recommandations
[Correctifs si nécessaire]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (tous les skills)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md, skills-coverage.md, skills-router.md
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]
