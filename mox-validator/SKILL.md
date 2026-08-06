---
name: mox-validator
description: >
  MOX — Gardien de coherence cross-repo.
  Valide les documents markdown (ADR, PRD, INTENT, EPIC) contre les schemas,
  detecte les contradictions, et loggue dans WAL.
version: "1.0.0"
status: active
intent_hash: 0xMOX_VALIDATOR_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: SKILLS/mox-validator/SKILL.md
triggers:
  - "valider document MOX"
  - "coherence cross-repo"
  - "detecter contradictions"
  - "MOX validation"
tools:
  - bash
  - read
  - grep
  - codebase_search
citizen: "MOX"
layer: "L4"
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

## Processus

### Etape 1 — Charger les schemas

```powershell
$artifactSchema = Get-Content "D:\DO\WEB\TOOLS\L0-CANON\REPO-STANDARDS\schemas\artifact-quality.schema.yaml" -Raw
$moxSchema = Get-Content "D:\DO\WEB\TOOLS\L0-CANON\REPO-STANDARDS\schemas\mox-coherence.schema.yaml" -Raw
```

### Etape 2 — Valider le frontmatter

- Verifier les champs obligatoires : type, version, status, date, intent_hash, citizen, layer, author, source_repo, source_path
- Valider contre artifact-quality.schema.yaml
- Verifier l'IntentHash : format `0x[A-Z0-9_]{8,}`

### Etape 3 — Valider la structure

- Sections obligatoires : objectif, contexte, perimetre, architecture, regles, roles, processus, probes, criteres, rollback, references
- Longueur max section : 15 lignes
- Longueur max phrase : 20 mots

### Etape 4 — Detecter les contradictions

- Comparer avec les documents existants
- Verifier les references croisees
- Detecter les doublons d'information

### Etape 5 — Logger dans WAL

```
[MOX] document=<path> status=PASS|FAIL issues=<list>
```

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Validation frontmatter | 100% | Schema JSON |
| Validation structure | 100% | Probe P-107 |
| Contradictions detectees | 0 non detectee | Cross-check |
| WAL log | 100% | WAL entry |

## Rollback

1. Revenir au document precedent.
2. Logger le revert dans WAL.
3. Corriger via PR review FLUX-D4.

## References

- `REPO-STANDARDS/schemas/artifact-quality.schema.yaml`
- `REPO-STANDARDS/schemas/mox-coherence.schema.yaml`
- `unified-design/atoms/GOVERNANCE/artifact-writing-standards.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
