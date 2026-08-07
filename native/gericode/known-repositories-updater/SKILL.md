---
name: known-repositories-updater
description: "Met a jour known_repositories.yaml a partir du registry GitHub ou d'une source externe."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KNOWN_REPOSITORIES_UPDATER_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/known-repositories-updater/SKILL.md
triggers:
  - "update known repositories"
  - "sync repos"
  - "refresh registry"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - known-repositories-updater

> **Verdict** : **SKILL D'EXECUTION** - Met a jour known_repositories.yaml.

---

## Objectif

Synchroniser known_repositories.yaml avec les repos GitHub reels.

---

## Declencheur

- Ajout d'un nouveau repo dans l'organisation gerivdb
- Suppression d'un repo dormant
- Mise a jour des chemins locaux

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
 | `github_org` | str | Organisation GitHub |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `report` | dict | Rapport de mise a jour |
 | `added` | list | Repos ajoutes |
 | `removed` | list | Repos supprimes |
 | `updated` | list | Repos mis a jour |

---

## Regles

1. Ne jamais supprimer un repo sans confirmation explicite
2. Toujours verifier le local_path avant d'ajouter
3. Preserver les metadonnees existantes (layer, status)

---

## Exemple d'usage

```python
from pathlib import Path
from known_repositories_updater import KnownRepositoriesUpdater

updater = KnownRepositoriesUpdater(
    known_repositories_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml"),
    github_org="gerivdb",
)
report = updater.update(dry_run=False)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_update_adds_new_repo` | Nouveau repo detecte | Ajoute |
 | `test_update_preserves_existing` | Repo existant | Conserve |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-912    known_repositories.yaml synchronise avec GitHub                    |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          known-repositories-updater fonctionne                           |
 | [OK]          P-912 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `GOVERNANCE-HUB/known_repositories.yaml`
