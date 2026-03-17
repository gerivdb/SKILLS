# TAXONOMY — Types de Skills Ecosystem-1

**Version** : 1.0.0 · **Date** : 2026-03-17

## Overview

Ce document définit la taxonomie canonique des types de Skills dans ecosystem-1. Tout skill déclaré dans le registre doit appartenir à l'une des catégories définies ci-dessous.

## Catégories de Skills

### 1. Foundational Skills (Compétences Fondamentales)

**Définition** : Skills transversaux applicables à tous les domaines métier. Ils ne sont pas spécifiques à un domaine particulier mais fournissent des capacités réutilisables.

**Critères d'éligibilité** :
- Réutilisable par ≥3 domaines différents
- Indépendant de tout domaine métier spécifique
- Applicable dans n'importe quel contexte de projet

**Exemples** :
- `product-context` : Contextualisation produit/audience
- `ecosystem-principles` : Principes ONTOLOGY, DRY, KISS, φ-CPS

### 2. Domain Skills (Compétences Métier)

**Définition** : Skills spécifiques à un domaine métier cohérent. Ils implémentent une logique métier identifiable et déployable indépendamment.

**Critères d'éligibilité** :
- Lié à un domaine métier distinct (booking, recruitment, finance, etc.)
- Cycle de vie indépendant du domaine
- Testable et déployable de manière autonome

**Exemples** :
- `booking` : Orchestration des réservations (GERIBOOKING)
- `recruitment` : Matching candidats (CANDIDATOR)
- `finance` : Analyse bancaire (BANK-BUSTER)
- `content` : Génération de contenu (FLUENCE + BRAIN)

### 3. External Skills (Compétences Externes)

**Définition** : Skills provenant de tiers, assimilés dans ecosystem-1 via un processus de citoyennisation.

**Critères d'éligibilité** :
- Provenance externe (autre dépôt GitHub, vendor, etc.)
- Licence compatible (MIT, Apache 2.0, BSD, etc.)
- Processus de validationpassed

**Processus d'assimilation** :
1. Évaluation de la licence
2. Mapping vers les skills natifs equivalents
3. Identification des gaps
4. Intégration via submodule
5. Documentation dans ASSIMILATION.md

**Exemples** :
- `marketingskills` : Compétences marketing de coreyhaines31

## Attributs des Skills

### Frontmatter Obligatoire

Chaque fichier SKILL.md doit inclure un frontmatter YAML avec les attributs suivants:

```yaml
---
name: skill-name
description: Description courte du skill
triggers:
  - trigger-1
  - trigger-2
domain: foundational|domain|external
version: 1.0.0
author: gerivdb|external
license: MIT|Apache-2.0|...
status: active|deprecated|draft
created: 2026-03-17
updated: 2026-03-17
---
```

### Attributs Détaillés

| Attribut | Type | Requis | Description |
|----------|------|--------|-------------|
| `name` | string | ✅ | Identifiant unique du skill |
| `description` | string | ✅ | Description courte (≤200 caractères) |
| `triggers` | array | ✅ | Mots-clés déclencheurs |
| `domain` | enum | ✅ | Type de skill (foundational/domain/external) |
| `version` | semver | ✅ | Version sémantique |
| `author` | string | ✅ | Propriétaire (gerivdb ou externe) |
| `license` | string | ✅ | Licence du skill |
| `status` | enum | ✅ | Statut (active/deprecated/draft) |
| `created` | date | ✅ | Date de création (YYYY-MM-DD) |
| `updated` | date | ✅ | Date de mise à jour (YYYY-MM-DD) |
| `tags` | array | ❌ | Tags additionnels |
| `deps` | array | ❌ | Dépendances vers d'autres skills |
| ` φ-weight` | float | ❌ | Pondération φ-CPS (par défaut: 0.001) |

## Règles de Nommage

### Conventions

- **Nom du skill** : kebab-case (ex: `product-context`, `ecosystem-principles`)
- **Fichier** : `SKILL.md` (obligatoire)
- **Répertoire** : Nom du skill (ex: `native/foundational/product-context/`)

### Restrictions

- ❌ Pas de majuscules dans les noms
- ❌ Pas d'espaces
- ❌ Pas de caractères spéciaux hors `-` et `_`
- ❌ Pas de duplication de nom

## Workflow de Déclaration

```
1. Créer le fichier SKILL.md avec frontmatter
2. Ajouter le skill dans REGISTRY.yaml
3. Exécuter validation locale: tools/validate-skills.sh
4. Soumettre PR avec CI green
5. Review par skills-registry citizen
6. Merge et publication automatique
```

## Governance

| Rôle | Responsabilité |
|------|----------------|
| **skills-registry (L2)** | Validation et approval des skills |
| **ecoystem-orchestrator (L5)** | Intégration dans ECOYSTEM |
| **governance-guardian (L3)** | Conformité taxonomie |

---

*Canonical document · Part of ecosystem-1 SKILLS registry*
