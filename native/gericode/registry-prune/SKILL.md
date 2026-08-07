---
name: registry-prune
description: "Nettoie les entrées orphelines dans tous les registres : REGISTRY.yaml, registry.json, citizens.yaml, BRIDGES.yaml."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_REGISTRY_PRUNE_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/registry-prune/SKILL.md
triggers:
  - "prune registry"
  - "clean registry"
  - "remove orphans"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill — registry-prune

> **Verdict** : **SKILL D'EXÉCUTION** — Nettoie les registres.

---

## Objectif

Supprimer les entrées orphelines dans tous les registres.

---

## Déclencheur

- Détection d'orphelins par bridge-auditor
- Détection de skills orphelins par skills-validator
- Nettoyage périodique

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `registry_yaml_path` | Path | Chemin vers REGISTRY.yaml |
 | `registry_json_path` | Path | Chemin vers registry.json |
 | `citizens_yaml_path` | Path | Chemin vers citizens.yaml |
 | `bridges_path` | Path | Chemin vers BRIDGES.yaml |
 | `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `pruned_entries` | dict | Entrées supprimées par registre |
 | `errors` | list | Erreurs |

---

## Règles

1. Ne jamais supprimer sans confirmation explicite (sauf dry_run)
2. Toujours sauvegarder avant suppression
3. Logger toutes les suppressions dans WAL

---

## Exemple d'usage

```python
from pathlib import Path
from registry_prune import RegistryPrune

prune = RegistryPrune(
    registry_yaml_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
    registry_json_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/registry.json"),
    citizens_yaml_path=Path("act-protocol/citizens.yaml"),
    bridges_path=Path("D:/DO/WEB/TOOLS/L1-INFRA/TOPOS/BRIDGES.yaml"),
    known_repositories_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml"),
)
report = prune.prune(dry_run=True)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_prune_orphan_skills` | Skills orphelins | Supprimés |
 | `test_prune_orphan_citizens` | Citizens orphelins | Supprimés |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-913    0 entrée orpheline dans REGISTRY.yaml                             |
 | P-914    0 entrée orpheline dans citizens.yaml                             |
 | P-915    0 entrée orpheline dans BRIDGES.yaml                              |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          registry-prune fonctionne                                        |
 | ✓          P-913 passe                                                      |
 | ✓          P-914 passe                                                      |
 | ✓          P-915 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `bridge-auditor`
 - `citizenship-auditor`
 - `skills-validator`
