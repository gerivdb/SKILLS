---
name: skills-agentic-test
version: "2.0.0"
description: "Suite de tests v2 pour valider le pipeline SKILLS_AGENTIC. Contient 30 requêtes de test (20 v1 + 10 v2) couvrant les cas nominaux, multi-intents, complexes cross-strate, edge cases, non-régression, et tests spécifiques v2 (délégation, reformulation, brouillon, feedback ciblé). Utiliser quand l'utilisateur mentionne 'test agentic', 'valider pipeline', 'SKILLS_AGENTIC test', 'couverture test', 'test v2', 'test délégation', 'test reformulation'."
triggers:
  - "test agentic"
  - "valider pipeline"
  - "SKILLS_AGENTIC test"
  - "couverture test"
  - "test coverage"
  - "test multi-skill"
  - "test v2"
  - "test délégation"
  - "test reformulation"
  - "test brouillon"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "skills-agentic.md (orchestrateur)"
  - "skills-coverage.md (vérificateur)"
  - "skills-router.md (routeur)"
  - "skills-rewriter.md (rewriter)"
  - "MANIFEST.json (SKILLS)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — 20 requêtes de test"}
  - {v: "2.0.0", date: "2026-06-07", notes: "v2 — +10 requêtes (délégation, reformulation, brouillon, feedback ciblé)"}
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

## Critères d'acceptation des tests v2

1. **30/30 requêtes** produisent les résultats attendus
2. **COVERAGE Agent** détecte 100% des gaps injectés
3. **Itération** : le pipeline converge en ≤3 itérations pour toutes les requêtes
4. **Non-régression** : les 63 skills existants continuent de fonctionner
5. **Traçabilité** : chaque test produit un log complet
6. **Délégation (v2)** : Le DELEGATOR identifie correctement le niveau sur 10 requêtes test
7. **Reformulation (v2)** : Le REWRITER produit des sous-quêtes matchant des skills (100% match)
8. **Brouillon (v2)** : Le DRAFT AGENT produit un brouillon structuré pour les niveaux 2+
9. **Feedback ciblé (v2)** : Le GAP ANALYZER génère un feedback avec skills recommandés (100% gaps)

## Catégorie F — Tests v2 : Délégation (4 requêtes)

| # | Requête | Niveau attendu | Justification |
|---|---------|----------------|---------------|
| F1 | "Vérifie FLUENCE" | 1 (Simple) | 1 intent, 1 strate, clair |
| F2 | "Scan emojis DevTools" | 1 (Simple) | 1 intent, 1 strate, clair |
| F3 | "Audit FLUENCE + conformité NEXUS" | 2 (Moyen) | 2 intents, 2 strates |
| F4 | "Audit BRAIN + ADR + PRD" | 2 (Moyen) | 3 intents, 2 strates |

## Catégorie G — Tests v2 : Reformulation (3 requêtes)

| # | Requête | Intent testé | Sous-quêtes attendues |
|---|---------|--------------|----------------------|
| G1 | "Audit structure FLUENCE" | audit_structure | scan_repo_structure, check_ddd_compliance, detect_epic_size_violations |
| G2 | "Vérifie conformité NEXUS" | verifier_conformite | validate_adr_format, check_phi_cps_threshold, audit_branch_governance |
| G3 | "Génère rapport FLUENCE" | generer_rapport | compile_audit_results, format_prd_output, publish_to_brain |

## Catégorie H — Tests v2 : Brouillon + Feedback ciblé (3 requêtes)

| # | Requête | Gaps injectés | Feedback ciblé attendu |
|---|---------|---------------|----------------------|
| H1 | "Audit FLUENCE (sans spécifier conformité)" | verifier_conformite manquant | "Il manque un skill de conformité. Recommandé : nexus-auditor" |
| H2 | "Vérifie structure + ADR (sans PRD)" | generer_rapport manquant | "Il manque un skill de génération. Recommandé : prd-factory ou workflow-orchestration" |
| H3 | "Audit complet sans scope" | Scope ambigu | "Le scope n'est pas défini. Demander clarification ou utiliser le repo courant" |

## Format de sortie des tests v2

```markdown
## SKILLS_AGENTIC_TEST v2 — Rapport

### Résumé
- Total : 30 (20 v1 + 10 v2)
- Pass : [N]
- Fail : [N]
- Coverage : [N]%

### Détails v2
| # | Catégorie | Requête | Niveau | Verdict | Brouillon | Feedback ciblé | Statut |
|---|-----------|---------|--------|---------|-----------|----------------|--------|
| F1 | Délégation | ... | 1 | SUFFICIENT | N/A | N/A | ✅ |
| G1 | Reformulation | ... | — | SUFFICIENT | Oui | N/A | ✅ |
| H1 | Brouillon+Gap | ... | — | INSUFFICIENT | Oui | Oui | ✅ |

### Gaps détectés
[Liste des gaps par requête]

### Recommandations
[Correctifs si nécessaire]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (tous les skills)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md, skills-coverage.md, skills-router.md, skills-rewriter.md
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]
