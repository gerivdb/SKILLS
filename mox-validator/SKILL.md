---
name: mox-validator
description: >
  MOX — Gardien de coherence cross-repo.
  Valide les documents markdown (ADR, PRD, INTENT, EPIC) contre les schemas,
  detecte les contradictions, classifie, convertit PRD->PRD_MOC, et loggue dans WAL.
  Implementation complete avec 14 processus.
version: "1.0.0"
status: active
intent_hash: 0xMOX_VALIDATOR_20260806
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: mox-validator/SKILL.md
triggers:
  - "valider document MOX"
  - "coherence cross-repo"
  - "detecter contradictions"
  - "classifier document"
  - "convertir PRD vers PRD_MOC"
  - "MOX validation"
tools:
  - bash
  - read
  - grep
  - codebase_search
citizen: "MOX"
layer: "L4"
implementation:
  language: Python
  package: mox_validator
  tests: tests/test_mox_validator.py
  bin: bin/mox-classify, bin/mox-convert, bin/mox-validate
---

# Skill — MOX Validator

> **Verdict** : **SKILL D'EXECUTION** — Gardien de coherence cross-repo.

---

## Objectif

Valider la coherence des documents markdown de l'ecosysteme et detecter les contradictions.

## Source de verite

| Source | Role |
|--------|------|
| `ONTOLOGY/ONTOLOGY.yaml` | SOT semantique |
| `REPO-STANDARDS/schemas/artifact-quality.schema.yaml` | Schema qualite |
| `REPO-STANDARDS/schemas/mox-coherence.schema.yaml` | Schema coherence MOX |
| `unified-design/atoms/GOVERNANCE/artifact-writing-standards.yaml` | Standards redaction |

## Implementation

### Package Python

```
mox-validator/
├── mox_validator/
│   ├── __init__.py          # MOXValidator class
│   └── ...
├── tests/
│   └── test_mox_validator.py
├── bin/
│   ├── mox-classify         # Classify document
│   ├── mox-convert          # Convert PRD -> PRD_MOC
│   └── mox-validate         # Full validation
└── SKILL.md
```

### Processus MOX (14 processus)

| # | Processus | Description | Implémentation |
|---|-----------|-------------|----------------|
| 1 | classify-document | Classifie un document par type | MOXValidator.classify_document() |
| 2 | convert-prd-to-moc | Convertit PRD en PRD MOC | MOXValidator.convert_prd_to_moc() |
| 3 | validate-delivery-plan | Valide le plan de livraison | MOXValidator.validate_delivery_plan() |
| 4 | validate-milestones | Valide les milestones | MOXValidator.validate_milestones() |
| 5 | validate-tests | Valide les tests par composant | MOXValidator.validate_tests() |
| 6 | validate-dependencies | Valide la matrice de dépendances | MOXValidator.validate_dependencies() |
| 7 | validate-risks | Valide le registre de risques | MOXValidator.validate_risks() |
| 8 | validate-frontmatter-schema | Valide frontmatter contre schéma | MOXValidator.validate_frontmatter_schema() |
| 9 | detect-cross-repo-contradictions | Détecte contradictions cross-repo | MOXValidator.detect_cross_repo_contradictions() |
| 10 | detect-gaps | Détecte les gaps dans documents | MOXValidator.detect_gaps() |
| 11 | detect-duplicates | Détecte duplications d'information | MOXValidator.detect_duplicates() |
| 12 | validate-probes | Valide probes P-101..P-109 | MOXValidator.validate_probes() |
| 13 | validate-ontology-terms | Valide termes ontologiques | MOXValidator._load_ontology() + check |
| 14 | log-wal | Log événements dans WAL | MOXValidator.log_wal() |

### Workflow MOX complet

```
[Document soumis] -> [classify-document] -> [determine-target-type] -> [convert-if-needed] -> [validate-frontmatter] -> [validate-structure] -> [validate-ontology] -> [validate-crossrefs] -> [validate-rss] -> [validate-artifact-quality] -> [detect-contradictions] -> [log-wal] -> [RESULT]
```

### CLI

```bash
# Classify
mox-classify <document_path>

# Convert PRD -> PRD_MOC
mox-convert <document_path> [output_path]

# Full validation
mox-validate <document_path> [--strict]
```

### Tests

```bash
python tests/test_mox_validator.py
```

Tests couverts :
- `test_classify_prd` — Classification PRD
- `test_classify_prd_moc` — Classification PRD_MOC
- `test_validate_frontmatter` — Validation frontmatter
- `test_validate_delivery_plan` — Validation plan de livraison
- `test_validate_milestones` — Validation milestones
- `test_validate_tests` — Validation tests
- `test_validate_dependencies` — Validation dépendances
- `test_validate_risks` — Validation risques
- `test_full_validation` — Pipeline complète
- `test_ontology_terms` — Chargement termes ontologiques

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Classification correcte | 100% | classify-document |
| Conversion PRD->PRD_MOC | 100% sections operationnelles | convert-prd-to-moc |
| Validation frontmatter | 100% | Schema JSON |
| Validation structure | 100% | Probe P-107 |
| Validation ontology | 100% | ontology-guardian |
| Validation crossrefs | 100% | Cross-check |
| Contradictions detectees | 0 non detectee | Cross-check |
| WAL log | 100% | WAL entry |

## Rollback

1. Identifier le document non conforme.
2. Restaurer depuis git.
3. Logger la violation dans WAL.
4. Corriger via PR review FLUX-D4.

## References

- `PRD-MOC-ACTPROTOCOL-DOCUMENT-CLASSIFICATION-MOX-EXTENSION.md`
- `REPO-STANDARDS/schemas/artifact-quality.schema.yaml`
- `REPO-STANDARDS/schemas/mox-coherence.schema.yaml`
- `unified-design/atoms/GOVERNANCE/artifact-writing-standards.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `SKILLS/ontology-guardian/`
- `SKILLS/artifact-quality-checker/`
