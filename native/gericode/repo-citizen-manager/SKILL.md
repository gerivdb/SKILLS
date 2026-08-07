---
name: repo-citizen-manager
description: "Gere la citoyennisation des repos de l'ecosysteme gerivdb. Transforme chaque repo en citoyen dote d'une identite ontologique, d'un verse VERSES, de bridges cross-repo et de plans consultables par MOX."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_REPO_CITIZEN_MANAGER_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/repo-citizen-manager/SKILL.md
triggers:
  - "citoyenniser repo"
  - "repo citizen"
  - "MOX consulter plans"
tools:
  - bash
  - read
  - write
citizen: "ECOSYSTEM-BRAIN"
layer: "L4"
---

# Skill - repo-citizen-manager

> **Verdict** : **SKILL D'EXECUTION** - Gere la citoyennisation des repos.

---

## Objectif

Gerer la citoyennisation des repos et l'enregistrement des skills :
- declarer le repo dans `citizens.yaml`,
- creer le verse dans `VERSES/verses/`,
- creer le bridge dans `BRIDGES.yaml`,
- enregistrer le skill dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\REGISTRY.yaml`.

 ---

 ## Declencheur

 - Citoyennisation d'un nouveau repo
 - Creation d'un nouveau skill dans `.kilo/skills/<repo>/`
 - MOX doit consulter les plans d'un repo
 - ARGUS detecte un gap de citoyennisation ou d'enregistrement de skill

 ---

 ## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `repo_name` | str | Nom du repo |
 | `skill_name` | str \| None | Nom du skill a enregistrer |
 | `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
 | `citizens_path` | Path | Chemin vers citizens.yaml |
 | `verses_dir` | Path | Repertoire des verses VERSES |
 | `skills_registry_path` | Path | Chemin vers SKILLS/REGISTRY.yaml |

 ---

 ## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `verse_path` | Path | Chemin du verse cree |
 | `citizen_registered` | bool | Citizen declare |
 | `bridge_created` | bool | Bridge cree |
 | `skill_registered` | bool | Skill enregistre dans REGISTRY.yaml |

 ---

 ## Regles

 1. Verifier que le repo existe dans `known_repositories.yaml`
 2. Verifier que le repo n'est pas deja un citoyen
 3. Creer le verse dans `VERSES/verses/`
 4. Declarer le citizen dans `citizens.yaml`
 5. Creer le bridge dans `BRIDGES.yaml`
 6. **Si un skill est fourni, l'enregistrer dans `SKILLS/REGISTRY.yaml` avec `source_repo`, `path` relatif et `source: native`**
 7. Logger dans WAL

 ---

 ## Exemple d'usage

 ```python
 from pathlib import Path
 from repo_citizen_manager import verify_repo, check_citizen, create_verse, register_citizen, register_skill

 known = Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml")
 citizens = Path("act-protocol/citizens.yaml")
 verses = Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/verses/")
 skills_registry = Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml")

 repo = "GeriCode"
 skill = "yaml-safe-injector"

 if verify_repo(repo, known) and not check_citizen(repo, citizens):
     create_verse(repo, verses)
     register_citizen(repo, citizens)
     if skill:
         register_skill(skill, skills_registry, source_repo="gerivdb/GeriCode")
 ```

---

## Tests

| Test | Description | Attend |
 |------|-------------|--------|
 | `test_verify_repo_exists` | Repo existe | True |
 | `test_verify_repo_missing` | Repo n'existe pas | False |
 | `test_check_citizen_true` | Citizen existe | True |
 | `test_check_citizen_false` | Citizen n'existe pas | False |
 | `test_create_verse` | Verse cree | Fichier existe |
 | `test_register_citizen` | Citizen declare | Ajoute dans YAML |
 | `test_register_skill` | Skill enregistre | Entree ajoutee dans REGISTRY.yaml |

 ---

 ## Reference ADR

- **ADR** : ADR-2026-08-07-008-REPO_CITIZEN_MANAGER
- **IntentHash** : 0xADR_REPO_CITIZEN_MANAGER_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `ECOSYSTEM-BRAIN` | Decouverte et citoyennisation |
| `PRIMUS` | Orchestration |
| `MOX` | Validation des citoyens |
| `ARGUS` | Detection des gaps |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-720    verify_repo detecte le repo dans known_repositories.yaml          |
| P-721    check_citizen detecte les citoyens declares                       |
| P-722    create_verse cree le fichier verse                                |
| P-723    register_citizen ajoute le citizen dans citizens.yaml              |
| P-724    register_skill ajoute le skill dans SKILLS/REGISTRY.yaml          |
+-----------------------------------------------------------------------------+
```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          verify_repo fonctionne                                          |
 | [OK]          check_citizen fonctionne                                         |
 | [OK]          create_verse cree le fichier                                     |
 | [OK]          register_citizen met a jour citizens.yaml                        |
 | [OK]          register_skill met a jour REGISTRY.yaml                          |
 +-----------------------------------------------------------------------------+
 ```

---

## Rollback

1. Supprimer le verse de `VERSES/verses/`.
2. Supprimer le citizen de `citizens.yaml`.
3. Supprimer le bridge de `BRIDGES.yaml`.
4. Logger dans WAL.

---

## References

- `repo-citizen-registry.yaml`
- `PRD-MOC-ACTPROTOCOL-HARNESS-ENGINEERING-2026-08-07.md`
- `ecosystem-probe`
