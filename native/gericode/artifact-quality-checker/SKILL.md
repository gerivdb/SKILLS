# Skill — artifact-quality-checker

> **IntentHash** : 0xSKILL_ARTIFACT_QUALITY_CHECKER_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L2b  
> **Status** : proposed  

## Objectif

Valider la qualité des artefacts de gouvernance (PRD, ADR, EPIC, INTENT, SPEC, REPORT, RPT, GUI, RUN)
et générer un rapport de conformité avec probes P-101 à P-109.

## Déclencheur

- Pre-commit hook sur tout artefact de gouvernance
- Validation avant merge PR
- Audit qualité périodique
- Requête N243 pour évaluation de document

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `artifact` | object | Artefact à valider : `path`, `type`, `content` |
| `probes` | list | Liste des probes à exécuter (défaut: P-101 à P-109) |
| `mode` | string | `STRICT` (tous probes requis) ou `WARN` (seulement obligatoires) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `report` | YAML | Rapport de validation avec scores par probe |
| `score` | float | Score global de qualité (0-1) |
| `wal_entry` | JSON | Entrée WAL pour traçabilité |

## Probes

| Probe | Condition | Expected |
|-------|-----------|----------|
| P-101 | Frontmatter présent | PASS |
| P-102 | Frontmatter valide contre schema | PASS |
| P-103 | IntentHash unique | PASS |
| P-104 | Sections obligatoires présentes | PASS |
| P-105 | Pas de contradiction cross-ref | PASS |
| P-106 | Probes P-101 à P-105 passent | PASS (obligatoire) |
| P-107 | Document conforme RSS-v2.1 | PASS (obligatoire) |
| P-108 | Sources tracées | PASS |
| P-109 | WAL entry créée | PASS |

## Étapes

### 1. Charger l'artefact

- Lire le fichier
- Extraire le frontmatter YAML
- Extraire le contenu Markdown
- Valider le chemin `source_path`

### 2. Exécuter les probes

Pour chaque probe :
- P-101 : Vérifier présence frontmatter
- P-102 : Valider frontmatter contre `artifact-quality.schema.yaml`
- P-103 : Vérifier unicité IntentHash dans ONTOLOGY
- P-104 : Vérifier sections obligatoires
- P-105 : Vérifier pas de contradiction cross-ref
- P-106 : Vérifier P-101 à P-105 passent
- P-107 : Vérifier conformité RSS-v2.1
- P-108 : Vérifier sources tracées
- P-109 : Créer entrée WAL

### 3. Calculer le score

- Score = (probes_passés / probes_total)
- Si mode STRICT : tous probes requis
- Si mode WARN : seulement P-106 et P-107 requis

### 4. Générer le rapport

- Format YAML
- Inclure : path, type, intent_hash, date, probes, score, result
- Si FAIL : lister les issues et recommandations

### 5. Logger dans WAL

- Entrée WAL : timestamp, artifact_path, intent_hash, score, result

## Dépendances

| Dépendance | Rôle | Version |
|------------|------|---------|
| artifact-quality.schema.yaml | Validation frontmatter | Latest |
| ONTOLOGY.yaml | Vérification IntentHash | Latest |
| NEXUS | WAL, traçabilité | Latest |
| MOX | Détection contradictions | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_probes_pass` | Document conforme | 100% probes passent |
| `test_probes_fail` | Document non conforme | P-106/P-107 échouent |
| `test_report_generated` | Rapport généré | Fichier YAML créé |

## Références

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > artifact-quality, MOX`
- Atom : `unified-design/atoms/governance/artifact-writing-standards.yaml`
- Schéma : `REPO-STANDARDS/schemas/artifact-quality.schema.yaml`
