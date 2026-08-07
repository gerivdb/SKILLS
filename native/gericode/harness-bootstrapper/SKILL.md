---
name: harness-bootstrapper
description: "Bootstrap le harness d'agent à partir des designs Harness/Hexagonal/DDD/DbC/ATDD/BDD."
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

# Skill — harness-bootstrapper

> **Verdict** : **SKILL D'EXÉCUTION** — Bootstrap le harness d'agent.

---

## Objectif

Générer la structure Hexagonal/DDD/DbC/ATDD/BDD complète pour un nouvel agent.

---

## Déclencheur

- Création d'un nouvel agent dans `.kilo/agent/<name>/`
- Refactoring d'un agent existant vers Hexagonal
- Initialisation d'un repo citoyen avec harness

---

## Structure générée

```
.kilo/agent/<name>/
├── domain/
│   ├── entities.py
│   ├── value_objects.py
│   ├── events.py
│   └── exceptions.py
├── application/
│   ├── ports/
│   │   ├── in/
│   │   └── out/
│   ├── services/
│   └── dto.py
├── infrastructure/
│   ├── adapters/
│   │   ├── in/
│   │   └── out/
│   └── config/
├── contracts/
│   ├── contracts.py
│   └── pre_conditions.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/
└── SKILL.md
```

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `agent_name` | str | Nom de l'agent |
 | `layer` | str | Couche logique (L0-L5) |
 | `domain` | str | Domaine fonctionnel |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `structure_path` | Path | Chemin de la structure créée |
 | `files_created` | list | Liste des fichiers créés |

---

## Règles

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
 | `test_bootstrap_agent` | Bootstrap complet | Structure créée |
 | `test_bootstrap_existing_agent` | Agent existant | Erreur |
 | `test_bootstrap_with_domain` | Domaine spécifié | DTO créé |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-910    Structure Hexagonal complète créée                                 |
 | P-911    Tous les fichiers DbC/BDD présents                                 |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          harness-bootstrapper fonctionne                                  |
 | ✓          P-910 passe                                                      |
 | ✓          P-911 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `hexagonal-architecture.yaml`
 - `ddd-domain-layer.yaml`
 - `harness-engineering.yaml`
