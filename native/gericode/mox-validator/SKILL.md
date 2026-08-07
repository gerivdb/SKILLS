# Skill - mox-validator

> **IntentHash** : 0xSKILL_MOX_VALIDATOR_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L2b  
> **Status** : proposed  

## Objectif

Garantir la meta-coherence des documents markdown de l'ecosysteme en validant
frontmatter, cross-references, bridges, RSS-v2.1 et qualite d'artefact via MOX.

## Declencheur

- Pre-commit hook sur tout document de gouvernance
- Validation avant merge PR
- Audit cross-repo periodique
- Requete N243 necessitant une validation de coherence

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `document` | object | Document a valider : `path`, `type`, `intent_hash` |
| `layers` | list | Couches de validation : `frontmatter`, `crossrefs`, `bridges`, `rss_v23`, `artifact_quality` |
| `mode` | string | `STRICT` (fail) ou `WARN` (avertissement) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `validation` | object | Resultat par couche : `PASS`/`FAIL`/`WARN` + issues |
| `result` | string | Resultat global : `PASS`/`FAIL`/`WARN` |
| `wal_entry` | JSON | Entree WAL pour tracabilite |

## Etapes

### 1. Valider le frontmatter

- Verifier les champs obligatoires : `type`, `version`, `status`, `date`, `intent_hash`, `citizen`, `layer`, `author`, `source_repo`, `source_path`
- Valider contre `artifact-quality.schema.yaml`
- Verifier que `intent_hash` est unique (pas de collision)
- Verifier que `source_repo` est declare dans ONTOLOGY.yaml

### 2. Valider la structure

- Verifier les sections obligatoires : `objectif`, `contexte`, `perimetre`, `architecture`, `regles`, `roles`, `processus`, `probes`, `criteres`, `rollback`, `references`
- Verifier la longueur max des sections
- Verifier la presence des probes P-106 et P-107 (obligatoires)

### 3. Valider les cross-references

- Verifier que tous les IntentHash references existent
- Verifier que les chemins `source_path` sont valides
- Detecter les references circulaires
- Verifier que les bridges cross-repo sont declares dans `ECOS_ROOT.json`

### 4. Valider les bridges

- Verifier que les bridges declares dans le document existent dans ONTOLOGY
- Verifier la coherence des directions (source -> target)
- Detecter les bridges orphelins

### 5. Valider la conformite RSS-v2.1

- Verifier le format des commits (Conventional Commits)
- Verifier la structure des dossiers (PRD/, INTENTS/, ADR/, etc.)
- Verifier les hooks git (pre-commit, commit-msg)

### 6. Detecter les contradictions

- Comparer le document avec les documents lies
- Detecter les contradictions de frontmatter (intent_hash, status)
- Detecter les contradictions de contenu (definitions, roles)
- Logger les contradictions dans WAL

### 7. Generer le rapport

- Rapport par couche : `PASS`/`FAIL`/`WARN`
- Liste des issues avec severite
- Recommandations de correction
- Entree WAL avec IntentHash du document valide

## Dependances

| Dependance | Role | Version |
|------------|------|---------|
| ONTOLOGY.yaml | Definitions concepts, entites | Latest |
| REPO-STANDARDS/schemas | artifact-quality.schema.yaml, mox-coherence.schema.yaml | Latest |
| NEXUS | WAL, tracabilite | Latest |
| PLIX | Codec `.piano-diff` pour propagation corrections | Latest |
| KIX | Application politiques de coherence | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_frontmatter_valid` | Frontmatter valide | PASS |
| `test_frontmatter_invalid` | Frontmatter invalide | FAIL |
| `test_structure_complete` | Structure complete | PASS |
| `test_structure_missing` | Section manquante | FAIL |
| `test_crossref_contradiction` | Contradiction cross-repo | Detectee |

## References

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > MOX, NEXUS, KIX, PLIX`
- Atom : `unified-design/atoms/governance/mox-meta-coherence.yaml`
- Schema : `REPO-STANDARDS/schemas/mox-coherence.schema.yaml`
