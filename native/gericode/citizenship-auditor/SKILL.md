---
name: citizenship-auditor
description: "Valide la coherence de la citoyennete : citizens.yaml <-> known_repositories.yaml <-> VERSES <-> REGISTRY.yaml."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_CITIZENSHIP_AUDITOR_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/citizenship-auditor/SKILL.md
triggers:
  - "audit citizenship"
  - "citizenship check"
  - "repo citizen audit"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - citizenship-auditor

> **Verdict** : **SKILL D'EXECUTION** - Audite la coherence de la citoyennete.

---

## Objectif

Valider P-801 a P-807 : tous les repos sont citoyens, tous les citoyens ont un verse, tous les skills sont dans REGISTRY.yaml.

---

## Declencheur

- CI/CD : audit automatique
- ARGUS : detection de gaps
- MOX : verification avant merge

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `known_repositories_path` | Path | `known_repositories.yaml` |
 | `citizens_yaml_path` | Path | `citizens.yaml` |
 | `verses_dir` | Path | `VERSES/verses/` |
 | `skills_dir` | Path | `.kilo/skills/` |
 | `registry_yaml_path` | Path | `SKILLS/REGISTRY.yaml` |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `audit_report` | dict | Rapport d'audit |
 | `errors` | list | Erreurs critiques |
 | `warnings` | list | Avertissements |

---

## Regles

1. P-801 : Tous les repos actifs sont des citoyens declares
2. P-802 : Tous les citoyens ont un verse dans VERSES/verses/
3. P-806 : Tout skill dans .kilo/skills/<repo>/ est declare dans REGISTRY.yaml
4. P-807 : REGISTRY.yaml reference source_repo pour chaque skill

---

## Exemple d'usage

```python
from pathlib import Path
from citizenship_auditor import CitizenshipAuditor

auditor = CitizenshipAuditor(
    known_repositories_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml"),
    citizens_yaml_path=Path("act-protocol/citizens.yaml"),
    verses_dir=Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/verses/"),
    skills_dir=Path(".kilo/skills"),
    registry_yaml_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
)

report = auditor.audit()
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_audit_p801_pass` | Tous repos sont citizens | Passe |
 | `test_audit_p802_fail` | Citizen sans verse | Echec |
 | `test_audit_p806_fail` | Skill non enregistre | Echec |
 | `test_audit_p807_fail` | Skill sans source_repo | Echec |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-801    Tous les repos actifs sont des citoyens declares                   |
 | P-802    Tous les citoyens ont un verse dans VERSES/verses/                |
 | P-806    Tout skill dans .kilo/skills/<repo>/ est declare dans REGISTRY.yaml |
 | P-807    REGISTRY.yaml reference source_repo pour les skills externes      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          citizenship-auditor fonctionne                                   |
 | [OK]          P-801 passe                                                      |
 | [OK]          P-802 passe                                                      |
 | [OK]          P-806 passe                                                      |
 | [OK]          P-807 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `repo-citizen-manager`
 - `registry-sync`
