---
name: kiva-ci-local
description: "Template et validation de .kiva/ci.yaml pour pipelines CI locales KIVA-CLI. Genere le template et valide la conformite."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KIVA_CI_LOCAL_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/kiva-ci-local/SKILL.md
triggers:
  - "kiva ci"
  - "local ci"
  - ".kiva/ci.yaml"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - kiva-ci-local

> **Verdict** : **SKILL D'EXECUTION** - Template et validation de `.kiva/ci.yaml`.

---

## Objectif

Generer et valider le fichier `.kiva/ci.yaml` pour pipelines CI locales.

---

## Declencheur

- Creation d'un nouveau pipeline CI
- Validation d'un pipeline existant

---

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `target_dir` | Path | Repertoire du repo |
| `stages` | list | Stages du pipeline |

---

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `ci_path` | Path | Chemin du fichier `.kiva/ci.yaml` |

---

## Regles

1. Stages obligatoires : lint, test, typecheck, validate
2. Hooks : pre_commit, post_merge
3. Aucune dependance cloud

---

## Exemple d'usage

```python
from pathlib import Path
from kiva_ci_local import generate_ci_yaml

generate_ci_yaml(Path("."))
```

---

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_generate_ci_yaml` | Genere `.kiva/ci.yaml` | Fichier cree |
| `test_ci_yaml_has_stages` | Verifie les stages | 4 stages |
| `test_ci_yaml_has_hooks` | Verifie les hooks | 2 hooks |

---

## Reference ADR

- **ADR** : ADR-2026-08-07-007-KIVA_CI_LOCAL
- **IntentHash** : 0xADR_KIVA_CI_LOCAL_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `DEV-EXPERIENCE` | Garant de la CI locale |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-730    .kiva/ci.yaml existe                                                |
| P-731    Stages lint/test/typecheck/validate presents                       |
| P-732    Hooks pre_commit/post_merge configures                              |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          .kiva/ci.yaml present                                             |
| [OK]          4 stages definis                                                  |
| [OK]          2 hooks configures                                                |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `.kiva/ci.yaml`.
2. Logger dans WAL.

---

## References

- `local-kiva-ci-template.yaml`
- `skill-creation-tdd.yaml`
