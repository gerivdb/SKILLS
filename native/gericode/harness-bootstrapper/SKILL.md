---
name: harness-bootstrapper
description: "Bootstrap le harness d'agent a partir des designs Harness/Hexagonal/DDD/DbC/ATDD/BDD."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_HARNESS_BOOTSTRAPPER_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/harness-bootstrapper/SKILL.md
triggers:
  - "bootstrap harness"
  - "new agent"
  - "scaffold agent"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - harness-bootstrapper

> **Verdict** : **SKILL D'EXECUTION** - Bootstrap le harness d'agent.

---

## Objectif

Generer la structure Hexagonal/DDD/DbC/ATDD/BDD complete pour un nouvel agent.

---

## Declencheur

- Creation d'un nouvel agent dans `.kilo/agent/<name>/`
- Refactoring d'un agent existant vers Hexagonal
- Initialisation d'un repo citoyen avec harness

---

## Structure generee

```
.kilo/agent/<name>/
|---- domain/
|   |---- entities.py
|   |---- value_objects.py
|   |---- events.py
|   `---- exceptions.py
|---- application/
|   |---- ports/
|   |   |---- in/
|   |   `---- out/
|   |---- services/
|   `---- dto.py
|---- infrastructure/
|   |---- adapters/
|   |   |---- in/
|   |   `---- out/
|   `---- config/
|---- contracts/
|   |---- contracts.py
|   `---- pre_conditions.py
|---- tests/
|   |---- unit/
|   |---- integration/
|   `---- acceptance/
`---- SKILL.md
```

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `agent_name` | str | Nom de l'agent |
 | `layer` | str | Couche logique (L0-L5) |
 | `domain` | str | Domaine fonctionnel |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `structure_path` | Path | Chemin de la structure creee |
 | `files_created` | list | Liste des fichiers crees |

---

## Regles

1. Tout nouveau code va dans `domain/` pur
2. Les ports sont dans `application/ports/`
3. Les adapters sont dans `infrastructure/adapters/`
4. Les contrats DbC sont dans `contracts/`
5. Les tests BDD sont dans `tests/acceptance/`

---

## Exemple d'usage

```python
from pathlib import Path
from harness_bootstrapper import HarnessBootstrapper

bootstrapper = HarnessBootstrapper(agent_path=Path(".kilo/agent/my-agent"))
result = bootstrapper.bootstrap(agent_name="my-agent", layer="L4", domain="ecosystem-tools")
print(result)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_bootstrap_agent` | Bootstrap complet | Structure creee |
 | `test_bootstrap_existing_agent` | Agent existant | Erreur |
 | `test_bootstrap_with_domain` | Domaine specifie | DTO cree |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-910    Structure Hexagonal complete creee                                 |
 | P-911    Tous les fichiers DbC/BDD presents                                 |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          harness-bootstrapper fonctionne                                  |
 | [OK]          P-910 passe                                                      |
 | [OK]          P-911 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `hexagonal-architecture.yaml`
 - `ddd-domain-layer.yaml`
 - `harness-engineering.yaml`
