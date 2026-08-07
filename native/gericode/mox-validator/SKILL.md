# Skill — mox-validator

> **IntentHash** : 0xSKILL_MOX_VALIDATOR_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L2b  
> **Status** : proposed  

## Objectif

Garantir la méta-cohérence des documents markdown de l'écosystème en validant
frontmatter, cross-references, bridges, RSS-v2.1 et qualité d'artefact via MOX.

## Déclencheur

- Pre-commit hook sur tout document de gouvernance
- Validation avant merge PR
- Audit cross-repo périodique
- Requête N243 nécessitant une validation de cohérence

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `document` | object | Document à valider : `path`, `type`, `intent_hash` |
| `layers` | list | Couches de validation : `frontmatter`, `crossrefs`, `bridges`, `rss_v23`, `artifact_quality` |
| `mode` | string | `STRICT` (fail) ou `WARN` (avertissement) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `validation` | object | Résultat par couche : `PASS`/`FAIL`/`WARN` + issues |
| `result` | string | Résultat global : `PASS`/`FAIL`/`WARN` |
| `wal_entry` | JSON | Entrée WAL pour traçabilité |

## Étapes

### 1. Valider le frontmatter

- Vérifier les champs obligatoires : `type`, `version`, `status`, `date`, `intent_hash`, `citizen`, `layer`, `author`, `source_repo`, `source_path`
- Valider contre `artifact-quality.schema.yaml`
- Vérifier que `intent_hash` est unique (pas de collision)
- Vérifier que `source_repo` est déclaré dans ONTOLOGY.yaml

### 2. Valider la structure

- Vérifier les sections obligatoires : `objectif`, `contexte`, `perimetre`, `architecture`, `regles`, `roles`, `processus`, `probes`, `criteres`, `rollback`, `references`
- Vérifier la longueur max des sections
- Vérifier la présence des probes P-106 et P-107 (obligatoires)

### 3. Valider les cross-references

- Vérifier que tous les IntentHash référencés existent
- Vérifier que les chemins `source_path` sont valides
- Détecter les références circulaires
- Vérifier que les bridges cross-repo sont déclarés dans `ECOS_ROOT.json`

### 4. Valider les bridges

- Vérifier que les bridges déclarés dans le document existent dans ONTOLOGY
- Vérifier la cohérence des directions (source → target)
- Détecter les bridges orphelins

### 5. Valider la conformité RSS-v2.1

- Vérifier le format des commits (Conventional Commits)
- Vérifier la structure des dossiers (PRD/, INTENTS/, ADR/, etc.)
- Vérifier les hooks git (pre-commit, commit-msg)

### 6. Détecter les contradictions

- Comparer le document avec les documents liés
- Détecter les contradictions de frontmatter (intent_hash, status)
- Détecter les contradictions de contenu (définitions, rôles)
- Logger les contradictions dans WAL

### 7. Générer le rapport

- Rapport par couche : `PASS`/`FAIL`/`WARN`
- Liste des issues avec sévérité
- Recommandations de correction
- Entrée WAL avec IntentHash du document validé

## Dépendances

| Dépendance | Rôle | Version |
|------------|------|---------|
| ONTOLOGY.yaml | Définitions concepts, entités | Latest |
| REPO-STANDARDS/schemas | artifact-quality.schema.yaml, mox-coherence.schema.yaml | Latest |
| NEXUS | WAL, traçabilité | Latest |
| PLIX | Codec `.piano-diff` pour propagation corrections | Latest |
| KIX | Application politiques de cohérence | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_frontmatter_valid` | Frontmatter valide | PASS |
| `test_frontmatter_invalid` | Frontmatter invalide | FAIL |
| `test_structure_complete` | Structure complète | PASS |
| `test_structure_missing` | Section manquante | FAIL |
| `test_crossref_contradiction` | Contradiction cross-repo | Détectée |

## Références

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > MOX, NEXUS, KIX, PLIX`
- Atom : `unified-design/atoms/governance/mox-meta-coherence.yaml`
- Schéma : `REPO-STANDARDS/schemas/mox-coherence.schema.yaml`
