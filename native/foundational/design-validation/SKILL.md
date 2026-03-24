---
name: design-validation
description: Interview socratique relentless sur tout plan ou design jusqu'à résolution complète de chaque branche de l'arbre de décisions
triggers:
  - grill-me
  - stress-test
  - design-review
  - validate-plan
  - challenge
  - interview-design
  - decision-tree
  - validate-architecture
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-25
updated: 2026-03-25
tags:
  - validation
  - design
  - interview
  - socratic
  - stress-test
  - decision-tree
phi_weight: 0.007
consumes_from:
  - ecosystem-principles
provides_to:
  - BRAIN
  - FLUENCE
  - CANDIDATOR
  - ECOYSTEM
---

# Design Validation — Grill Me

## Description

Ce skill fondateur active un mode d'interview socratique relentless. L'agent interviewe l'utilisateur sur chaque aspect d'un plan ou design, parcourt chaque branche de l'arbre de décisions une par une, résout les dépendances entre décisions, et fournit sa réponse recommandée à chaque question. Activer avec `grill-me` ou toute variante.

## Protocole d'activation

```
Triggers : "grill me", "stress-test mon plan", "valide ce design",
           "challenge cette architecture", "interview-design"
```

## Comportement agent

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

**Règle fondamentale** : Pour chaque question, fournis ta réponse recommandée.

Si une question peut être répondue en explorant le codebase, explore le codebase d'abord.

## Arbre de décisions — Structure

```
Plan/Design
├── Branche 1 : Objectifs & Périmètre
│   ├── Question → [Réponse recommandée agent]
│   └── Dépendances résolues avant de continuer
├── Branche 2 : Architecture & Composants
│   ├── Question → [Réponse recommandée agent]
│   └── Dépendances résolues
├── Branche 3 : Contraintes & Risques
│   ├── Question → [Réponse recommandée agent]
│   └── ENV2/Z600 compliance check systématique
├── Branche 4 : Intégration ECOS
│   ├── φ-CPS delta estimé → validation
│   ├── ζ-DAG anchoring → identification
│   └── ONTOLOGY cohérence → vérification
└── Branche 5 : Critères d'acceptation
    ├── Question → [Réponse recommandée agent]
    └── Definition of Done validée
```

## Application dans ecosystem-1

### BRAIN — Validation d'architectures

```
Usage : "Grill me sur cette architecture BRAIN-v2"
Branches prioritaires : composants, dépendances, φ-CPS impact
Réponse recommandée : toujours ancrée dans ONTOLOGY + ENV2 constraints
```

### FLUENCE — Stress-test de stratégies contenu

```
Usage : "Stress-test mon plan de contenu Q2"
Branches prioritaires : audience, canaux, métriques, cohérence produit
Réponse recommandée : basée sur product-context skill
```

### CANDIDATOR — Validation de critères de matching

```
Usage : "Challenge mes critères de scoring candidat"
Branches prioritaires : critères, pondérations, edge cases, biais
Réponse recommandée : alignée avec domain/recruitment skill
```

### ECOYSTEM — Review gates constitutionnels

```
Usage : "Grill me avant ce merge EMIT"
Branches prioritaires : φ-CPS delta, ζ-DAG, ONTOLOGY, rollback plan
Réponse recommandée : verdict OK/KO/PARTIEL avec justification
```

## Questions types par branche

### Branche Objectifs
- Quel problème précis ce plan résout-il ? → *[Recommandation : définir en 1 phrase le job-to-be-done]*
- Qui sont les consommateurs directs ? → *[Recommandation : lister les citoyens L1-L5 impactés]*
- Quel est le critère de succès mesurable ? → *[Recommandation : une métrique φ-CPS ou KPI métier]*

### Branche Architecture
- Quels composants existants sont réutilisés ? → *[Recommandation : auditer CROSS_REPO_MATRIX.json d'abord]*
- Quelles nouvelles dépendances sont introduites ? → *[Recommandation : max 2 nouvelles dépendances, justifier chacune]*
- La contrainte ENV2 (8GB RAM max runtime) est-elle respectée ? → *[Recommandation : profiler avant tout commit]*

### Branche Risques
- Quel est le pire scénario de failure ? → *[Recommandation : définir rollback < 30min]*
- Y a-t-il une dette technique introduite ? → *[Recommandation : documenter dans ADR si > 2h de remboursement]*
- Le principe φ-CPS reste-t-il sous le budget max ? → *[Recommandation : vérifier ECOS_ROOT.json avant merge]*

### Branche Intégration ECOS
- Le ζ-DAG est-il mis à jour ? → *[Recommandation : edge SKILLS→[repo] obligatoire dans CROSS_REPO_MATRIX]*
- L'ONTOLOGY est-elle cohérente ? → *[Recommandation : vérifier TAXONOMY.md avant naming]*
- Le CI/CD est-il prêt ? → *[Recommandation : validate-skills.yml ou équivalent doit être green]*

## Règles du protocole

1. **Une question à la fois** — jamais de liste de questions en rafale
2. **Recommandation systématique** — chaque question s'accompagne d'une réponse agent recommandée
3. **Branche par branche** — ne pas passer à la branche N+1 avant résolution de N
4. **Codebase d'abord** — si la réponse est dans le code, l'explorer avant de demander
5. **Shared understanding** — l'interview se termine quand toutes les branches sont résolues

## ENV2 Compliance

```yaml
ram_runtime_mb: 0
vram_mb: null
docker_required: false
local_only: true
verdict: OK
note: Fichier Markdown pur, aucun runtime
```

## Dépendances

### Dépend de
- `ecosystem-principles` (fondational) — principles ONTOLOGY, φ-CPS, ζ-DAG

### Requis par
- BRAIN (architecture review)
- FLUENCE (strategy stress-test)
- CANDIDATOR (scoring criteria validation)
- ECOYSTEM (constitutional review gates)

## Changelog

- 1.0.0 (2026-03-25) — Version initiale, assimilation pattern grill-me

---

*Skill natif gerivdb · Part du registre SKILLS ecosystem-1 · Closes #1*
