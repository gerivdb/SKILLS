---
name: registry-sync
description: "Synchronise REGISTRY.yaml, registry.json et citizens.yaml pour garantir la cohérence multi-registres de l'écosystème."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_REGISTRY_SYNC_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/registry-sync/SKILL.md
triggers:
  - "sync registries"
  - "registry sync"
  - "synchronize skills"
  - "registry coherence"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill — registry-sync

> **Verdict** : **SKILL D'EXÉCUTION** — Synchronise les registres de l'écosystème.

---

## Objectif

Garantir la cohérence entre `REGISTRY.yaml`, `registry.json` et `citizens.yaml`.

---

## Déclencheur

- Désynchronisation détectée entre registres
- CI/CD : validation avant commit
- ARGUS : détection de gaps

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `registry_yaml_path` | Path | Chemin vers `SKILLS/REGISTRY.yaml` |
 | `registry_json_path` | Path | Chemin vers `SKILLS/registry.json` |
 | `citizens_yaml_path` | Path | Chemin vers `citizens.yaml` |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `sync_report` | dict | Rapport de synchronisation |
 | `errors` | list | Erreurs détectées |
 | `fixed` | bool | True si des corrections ont été appliquées |

---

## Règles

1. `REGISTRY.yaml` est la source de vérité
2. `registry.json` est régénéré à partir de `REGISTRY.yaml`
3. `citizens.yaml` est enrichi avec les repo citizens de `REGISTRY.yaml`
4. Toute modification est tracée dans WAL

---

## Exemple d'usage

```python
from pathlib import Path
from registry_sync import RegistrySyncEngine

engine = RegistrySyncEngine(
    registry_yaml=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
    registry_json=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/registry.json"),
    citizens_yaml=Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/citizens.yaml"),
)

report = engine.sync(dry_run=False)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_sync_registry_yaml_to_json` | REGISTRY.yaml → registry.json | JSON mis à jour |
 | `test_sync_citizens_from_registry` | REGISTRY.yaml → citizens.yaml | Citizens enrichis |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |
 | `test_detect_missing_source_repo` | Skill sans source_repo | Erreur P-807 |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-901    REGISTRY.yaml et registry.json ont même nombre de skills          |
 | P-902    citizens.yaml contient tous les repo citizens de REGISTRY.yaml    |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          registry-sync fonctionne                                         |
 | ✓          P-901 passe                                                      |
 | ✓          P-902 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Rollback

 1. `git checkout -- REGISTRY.yaml registry.json citizens.yaml`
 2. Restaurer depuis le dernier commit

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `yaml-safe-injector`
 - `sot-registry-guardian`
