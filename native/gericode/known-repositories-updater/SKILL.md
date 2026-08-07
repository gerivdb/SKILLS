---
name: known-repositories-updater
description: "Met à jour known_repositories.yaml à partir du registry GitHub ou d'une source externe."
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

# Skill — known-repositories-updater

> **Verdict** : **SKILL D'EXÉCUTION** — Met à jour known_repositories.yaml.

---

## Objectif

Synchroniser known_repositories.yaml avec les repos GitHub réels.

---

## Déclencheur

- Ajout d'un nouveau repo dans l'organisation gerivdb
- Suppression d'un repo dormant
- Mise à jour des chemins locaux

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
 | `github_org` | str | Organisation GitHub |
 | `dry_run` | bool | Si True, ne modifie rien |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `report` | dict | Rapport de mise à jour |
 | `added` | list | Repos ajoutés |
 | `removed` | list | Repos supprimés |
 | `updated` | list | Repos mis à jour |

---

## Règles

1. Ne jamais supprimer un repo sans confirmation explicite
2. Toujours vérifier le local_path avant d'ajouter
3. Préserver les métadonnées existantes (layer, status)

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
 | `test_update_adds_new_repo` | Nouveau repo détecté | Ajouté |
 | `test_update_preserves_existing` | Repo existant | Conservé |
 | `test_dry_run_no_changes` | dry_run=True | Aucune modification |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-912    known_repositories.yaml synchronisé avec GitHub                    |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          known-repositories-updater fonctionne                           |
 | ✓          P-912 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `GOVERNANCE-HUB/known_repositories.yaml`
