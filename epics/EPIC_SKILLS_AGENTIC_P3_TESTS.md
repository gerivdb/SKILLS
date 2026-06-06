# EPIC — SKILLS_AGENTIC Phase 3 : Tests et Validation

**ID** : EPIC-SKILLS-AGENTIC-003
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT — dépend de EPIC-SKILLS-AGENTIC-001 et 002
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_P3_20260606`

---

## 1. Vision

Créer une suite de tests complète pour valider le pipeline SKILLS_AGENTIC. Les tests couvrent : la décomposition des requêtes (PARSER), la sélection des skills (PLANNER), le routing cross-repo (ROUTER), la détection de couverture (COVERAGE), et l'itération (ITERATOR). L'objectif : **100% de détection des gaps** sur un jeu de 20 requêtes complexes.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `skills-agentic-test.md`** | Skill de test dédié au pipeline agentic |
| **Jeu de 20 requêtes de test** | 20 requêtes multi-intents couvrant les cas nominaux, edge cases, et échecs |
| **Matrice de couverture** | Matrice skills × intents montrant quels skills couvrent quels intents |
| **Tests de non-régression** | Vérifier que les 59 skills existants ne sont pas impactés |
| **Validation du COVERAGE Agent** | Le COVERAGE Agent doit détecter 100% des gaps injectés |

---

## 3. Périmètre

### Inclus
- `perplexity/skills/skills-agentic-test.md` — skill de test
- `tests/agentic/` — dossier de tests avec les 20 requêtes et résultats attendus
- Matrice de couverture skills × intents
- Tests de non-régression

### Exclus
- Tests de performance/latence (hors scope — dépend de l'infrastructure Perplexity)
- Tests d'intégration avec les 185 repos (trop complexe pour cette phase)

---

## 4. Livrables

| ID | Fichier | Description | Slots |
|----|---------|-------------|-------|
| L3.1 | `perplexity/skills/skills-agentic-test.md` | Skill de test — valide le pipeline agentic | +1 |
| L3.2 | `tests/agentic/test-queries.json` | 20 requêtes de test avec résultats attendus | 0 |
| L3.3 | `tests/agentic/coverage-matrix.json` | Matrice skills × intents | 0 |
| L3.4 | `tests/agentic/results/` | Résultats des tests (générés) | 0 |

**Impact total** : +1 slot (de 62 → 63)

---

## 5. Critères d'acceptation

1. **20 requêtes de test** : Couvrent les cas suivants :
   - 5 requêtes mono-intent (cas nominal)
   - 5 requêtes multi-intents (2-3 intents)
   - 5 requêtes complexes (4+ intents, cross-strate)
   - 3 requêtes edge case (ambiguës, contradictoires, hors scope)
   - 2 requêtes de non-régression (skills existants)
2. **Matrice de couverture** : Chaque skill est mappé à ses intents couverts
3. **COVERAGE Agent** : Détecte 100% des gaps injectés dans les requêtes de test
4. **Itération** : Le pipeline converge en ≤3 itérations pour toutes les requêtes
5. **Non-régression** : Les 59 skills existants continuent de fonctionner
6. **Format** : Le skill de test passe le lint YAML

---

## 6. Jeu de 20 Requêtes de Test

### Catégorie A — Mono-intent (5 requêtes)
| # | Requête | Skills attendus |
|---|---------|-----------------|
| A1 | "Vérifie la conformité NEXUS du repo FLUENCE" | nexus-auditor, reposcope-run |
| A2 | "Génère un PRD pour la fonctionnalité X" | prd-factory |
| A3 | "Scanne les emojis dans DevTools" | (skill existant) |
| A4 | "Vérifie les hooks git dans ECOYSTEM" | (skill existant) |
| A5 | "Analyse l'architecture de BRAIN" | reposcope-run |

### Catégorie B — Multi-intents (5 requêtes)
| # | Requête | Skills attendus |
|---|---------|-----------------|
| B1 | "Audit FLUENCE + vérifie conformité NEXUS" | reposcope-run, nexus-auditor |
| B2 | "Crée PRD + vérifie OKR consistency" | prd-factory, nexus-core |
| B3 | "Scanne emojis + génère rapport + corrige" | (skills existants) |
| B4 | "Audit BRAIN + vérifie ADR + génère PRD" | reposcope-run, adr-manager, prd-factory |
| B5 | "Vérifie structure + conformité + hooks" | reposcope-run, nexus-auditor, (hooks) |

### Catégorie C — Complexes cross-strate (5 requêtes)
| # | Requête | Skills attendus |
|---|---------|-----------------|
| C1 | "Audit complet FLUENCE : structure, conformité NEXUS, ADR, PRD, rapport" | reposcope-run, nexus-auditor, adr-manager, prd-factory, workflow-orchestration |
| C2 | "Migration repo X : scan, plan, exécute, vérifie" | reposcope-run, nexus-reformer, (migration) |
| C3 | "Gouvernance globale : NEXUS, ONTOLOGY, BRAIN, FLUENCE" | nexus-core, (ontology), reposcope-run |
| C4 | "Refactoring cross-repo : analyse, plan, exécute, valide" | reposcope-run, nexus-reformer, skill-tester |
| C5 | "Conformité totale : structure, ADR, PRD, OKR, hooks, emojis" | Tous les skills de conformité |

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

---

## 7. Dépendances

| Dépendance | Type | Statut |
|------------|------|--------|
| EPIC-SKILLS-AGENTIC-001 (Phase 1) | Précédence | ⏳ En cours |
| EPIC-SKILLS-AGENTIC-002 (Phase 2) | Précédence | ⏳ En attente |
| 59 skills existants | Contexte de test | ✅ Existants |
| `known_repositories.yaml` | Source de vérité routing | ✅ Existant |

---

## 8. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Créer `skills-agentic-test.md` | 2h |
| Rédiger les 20 requêtes de test | 2h |
| Construire la matrice de couverture | 1h |
| Exécuter les tests et documenter | 2h |
| **Total** | **7h (1 jour)** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_AGENTIC_P3_20260606`*
