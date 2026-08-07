# Skill - artifact-quality-checker

> **IntentHash** : 0xSKILL_ARTIFACT_QUALITY_CHECKER_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L2b  
> **Status** : proposed  

## Objectif

Valider la qualite des artefacts de gouvernance (PRD, ADR, EPIC, INTENT, SPEC, REPORT, RPT, GUI, RUN)
et generer un rapport de conformite avec probes P-101 a P-109.

## Declencheur

- Pre-commit hook sur tout artefact de gouvernance
- Validation avant merge PR
- Audit qualite periodique
- Requete N243 pour evaluation de document

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `artifact` | object | Artefact a valider : `path`, `type`, `content` |
| `probes` | list | Liste des probes a executer (defaut: P-101 a P-109) |
| `mode` | string | `STRICT` (tous probes requis) ou `WARN` (seulement obligatoires) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `report` | YAML | Rapport de validation avec scores par probe |
| `score` | float | Score global de qualite (0-1) |
| `wal_entry` | JSON | Entree WAL pour tracabilite |

## Probes

| Probe | Condition | Expected |
|-------|-----------|----------|
| P-101 | Frontmatter present | PASS |
| P-102 | Frontmatter valide contre schema | PASS |
| P-103 | IntentHash unique | PASS |
| P-104 | Sections obligatoires presentes | PASS |
| P-105 | Pas de contradiction cross-ref | PASS |
| P-106 | Probes P-101 a P-105 passent | PASS (obligatoire) |
| P-107 | Document conforme RSS-v2.1 | PASS (obligatoire) |
| P-108 | Sources tracees | PASS |
| P-109 | WAL entry creee | PASS |

## Etapes

### 1. Charger l'artefact

- Lire le fichier
- Extraire le frontmatter YAML
- Extraire le contenu Markdown
- Valider le chemin `source_path`

### 2. Executer les probes

Pour chaque probe :
- P-101 : Verifier presence frontmatter
- P-102 : Valider frontmatter contre `artifact-quality.schema.yaml`
- P-103 : Verifier unicite IntentHash dans ONTOLOGY
- P-104 : Verifier sections obligatoires
- P-105 : Verifier pas de contradiction cross-ref
- P-106 : Verifier P-101 a P-105 passent
- P-107 : Verifier conformite RSS-v2.1
- P-108 : Verifier sources tracees
- P-109 : Creer entree WAL

### 3. Calculer le score

- Score = (probes_passes / probes_total)
- Si mode STRICT : tous probes requis
- Si mode WARN : seulement P-106 et P-107 requis

### 4. Generer le rapport

- Format YAML
- Inclure : path, type, intent_hash, date, probes, score, result
- Si FAIL : lister les issues et recommandations

### 5. Logger dans WAL

- Entree WAL : timestamp, artifact_path, intent_hash, score, result

## Dependances

| Dependance | Role | Version |
|------------|------|---------|
| artifact-quality.schema.yaml | Validation frontmatter | Latest |
| ONTOLOGY.yaml | Verification IntentHash | Latest |
| NEXUS | WAL, tracabilite | Latest |
| MOX | Detection contradictions | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_probes_pass` | Document conforme | 100% probes passent |
| `test_probes_fail` | Document non conforme | P-106/P-107 echouent |
| `test_report_generated` | Rapport genere | Fichier YAML cree |

## References

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > artifact-quality, MOX`
- Atom : `unified-design/atoms/governance/artifact-writing-standards.yaml`
- Schema : `REPO-STANDARDS/schemas/artifact-quality.schema.yaml`
