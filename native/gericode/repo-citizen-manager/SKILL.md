---
name: repo-citizen-manager
description: "Gère la citoyennisation des repos de l'écosystème gerivdb. Transforme chaque repo en citoyen doté d'une identité ontologique, d'un verse VERSES, de bridges cross-repo et de plans consultables par MOX."
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

# Skill — repo-citizen-manager

> **Verdict** : **SKILL D'EXÉCUTION** — Gère la citoyennisation des repos.

---

## Objectif

Gérer la citoyennisation des repos et l'enregistrement des skills :
- déclarer le repo dans `citizens.yaml`,
- créer le verse dans `VERSES/verses/`,
- créer le bridge dans `BRIDGES.yaml`,
- enregistrer le skill dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\REGISTRY.yaml`.

 ---

 ## Déclencheur

 - Citoyennisation d'un nouveau repo
 - Création d'un nouveau skill dans `.kilo/skills/<repo>/`
 - MOX doit consulter les plans d'un repo
 - ARGUS détecte un gap de citoyennisation ou d'enregistrement de skill

 ---

 ## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `repo_name` | str | Nom du repo |
 | `skill_name` | str \| None | Nom du skill à enregistrer |
 | `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
 | `citizens_path` | Path | Chemin vers citizens.yaml |
 | `verses_dir` | Path | Répertoire des verses VERSES |
 | `skills_registry_path` | Path | Chemin vers SKILLS/REGISTRY.yaml |

 ---

 ## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `verse_path` | Path | Chemin du verse créé |
 | `citizen_registered` | bool | Citizen déclaré |
 | `bridge_created` | bool | Bridge créé |
 | `skill_registered` | bool | Skill enregistré dans REGISTRY.yaml |

 ---

 ## Règles

 1. Vérifier que le repo existe dans `known_repositories.yaml`
 2. Vérifier que le repo n'est pas déjà un citoyen
 3. Créer le verse dans `VERSES/verses/`
 4. Déclarer le citizen dans `citizens.yaml`
 5. Créer le bridge dans `BRIDGES.yaml`
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
 | `test_create_verse` | Verse créé | Fichier existe |
 | `test_register_citizen` | Citizen déclaré | Ajouté dans YAML |
 | `test_register_skill` | Skill enregistré | Entrée ajoutée dans REGISTRY.yaml |

 ---

 ## Référence ADR

- **ADR** : ADR-2026-08-07-008-REPO_CITIZEN_MANAGER
- **IntentHash** : 0xADR_REPO_CITIZEN_MANAGER_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `ECOSYSTEM-BRAIN` | Découverte et citoyennisation |
| `PRIMUS` | Orchestration |
| `MOX` | Validation des citoyens |
| `ARGUS` | Détection des gaps |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-720    verify_repo détecte le repo dans known_repositories.yaml          |
| P-721    check_citizen détecte les citoyens déclarés                       |
| P-722    create_verse crée le fichier verse                                |
| P-723    register_citizen ajoute le citizen dans citizens.yaml              |
| P-724    register_skill ajoute le skill dans SKILLS/REGISTRY.yaml          |
+-----------------------------------------------------------------------------+
```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          verify_repo fonctionne                                          |
 | ✓          check_citizen fonctionne                                         |
 | ✓          create_verse crée le fichier                                     |
 | ✓          register_citizen met à jour citizens.yaml                        |
 | ✓          register_skill met à jour REGISTRY.yaml                          |
 +-----------------------------------------------------------------------------+
 ```

---

## Rollback

1. Supprimer le verse de `VERSES/verses/`.
2. Supprimer le citizen de `citizens.yaml`.
3. Supprimer le bridge de `BRIDGES.yaml`.
4. Logger dans WAL.

---

## Références

- `repo-citizen-registry.yaml`
- `PRD-MOC-ACTPROTOCOL-HARNESS-ENGINEERING-2026-08-07.md`
- `ecosystem-probe`
