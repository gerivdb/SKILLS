---
name: artifact-quality-checker
description: >
  Verifie la qualite des artefacts de gouvernance (PRD, ADR, EPIC, INTENT)
  selon les probes P-101..P-109. Bloque les non-conformites.
  Implementation complete avec MOXValidator backend.
version: "1.0.0"
status: active
intent_hash: 0xARTIFACT_QUALITY_CHECKER_20260806
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: artifact-quality-checker/SKILL.md
triggers:
  - "verifier qualite artefact"
  - "probes P-101 P-109"
  - "artifact quality"
  - "MOX validation"
tools:
  - bash
  - read
  - grep
citizen: "MOX"
layer: "L4"
implementation:
  language: Python
  package: mox_validator
  bin: bin/artifact-quality-check
---

# Skill — Artifact Quality Checker

> **Verdict** : **SKILL D'EXECUTION** — Verifie la qualite des artefacts de gouvernance.

---

## Objectif

Verifier que les artefacts respectent les standards de redaction (P-101..P-109).

## Implementation

### Backend

Utilise `mox_validator.MOXValidator` pour :
- `validate_probes()` — P-101..P-109
- `validate_frontmatter_schema()` — P-106
- `detect_gaps()` — P-107

### CLI

```bash
artifact-quality-check <document_path>
```

Sortie JSON :
```json
{
  "document": "<path>",
  "valid": true|false,
  "probes": {
    "P-101": "PASS|FAIL",
    "P-102": "PASS|FAIL",
    ...
    "P-109": "PASS|FAIL"
  },
  "issues": [...]
}
```

### Processus

| Probe | Verification |
|-------|--------------|
| P-101 | Longueur moyenne phrase <= 20 mots |
| P-102 | Longueur max section <= 15 lignes |
| P-103 | Items par liste <= 8 |
| P-104 | >= 1 tableau ASCII par section donnees/processus |
| P-105 | >= 1 reference explicite par section reference |
| P-106 | Frontmatter valide (schema JSON) |
| P-107 | Sections obligatoires presentes |
| P-108 | 0 digression cross-artefact |
| P-109 | 0 duplication information |

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Probes passantes | 100% (P-106, P-107 obligatoires) | Verification |
| Rapport genere | 1 par document | Fichier JSON |
| Issues loggees | 0 si PASS | WAL entry |

## Rollback

1. Revenir au document precedent.
2. Logger le revert dans WAL.
3. Corriger via PR review MOX.

## References

- `unified-design/atoms/GOVERNANCE/artifact-writing-standards.yaml`
- `REPO-STANDARDS/schemas/artifact-quality.schema.yaml`
- `REPO-STANDARDS/templates/PRD_template.md`
- `SKILLS/mox-validator/`
