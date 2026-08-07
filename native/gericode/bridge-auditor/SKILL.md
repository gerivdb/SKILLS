---
name: bridge-auditor
description: "Valide BRIDGES.yaml : détecte les bridges orphelins, manquants et les cycles."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_BRIDGE_AUDITOR_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/bridge-auditor/SKILL.md
triggers:
  - "audit bridges"
  - "bridge check"
  - "topology audit"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill — bridge-auditor

> **Verdict** : **SKILL D'EXÉCUTION** — Audite les bridges cross-repo.

---

## Objectif

Valider BRIDGES.yaml : détecter les bridges orphelins, manquants et les cycles.

---

## Déclencheur

- CI/CD : validation avant commit
- ARGUS : détection d'anomalies topologiques
- MOX : vérification avant merge

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `bridges_path` | Path | Chemin vers `TOPOS/BRIDGES.yaml` |
 | `known_repositories_path` | Path | Chemin vers `known_repositories.yaml` |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `audit_report` | dict | Rapport d'audit |
 | `orphaned_bridges` | list | Bridges orphelins |
 | `missing_bridges` | list | Repos sans bridge |
 | `cycles` | list | Cycles détectés |

---

## Règles

1. Tous les bridges référencent des repos existants dans known_repositories.yaml
2. Tous les repos actifs ont un bridge
3. Pas de cycles dans les bridges

---

## Exemple d'usage

```python
from pathlib import Path
from bridge_auditor import BridgeAuditor

auditor = BridgeAuditor(
    bridges_path=Path("D:/DO/WEB/TOOLS/L1-INFRA/TOPOS/BRIDGES.yaml"),
    known_repositories_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml"),
)

report = auditor.audit()
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_audit_no_orphans` | Pas d'orphelins | Liste vide |
 | `test_audit_no_missing` | Pas de manquants | Liste vide |
 | `test_audit_no_cycles` | Pas de cycles | Liste vide |
 | `test_audit_with_orphans` | Avec orphelins | Détectés |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-905    0 bridge orphelin                                                  |
 | P-906    0 cycle dans BRIDGES.yaml                                          |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          bridge-auditor fonctionne                                        |
 | ✓          P-905 passe                                                      |
 | ✓          P-906 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `sot-registry-guardian`
 - `repo-citizen-manager`
