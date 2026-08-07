---
name: skill-auto-enroller
description: "Pipeline 1-clic : verifie le repo, cree le verse, enregistre le citizen, cree le bridge, inscrit le skill dans REGISTRY.yaml, et optionnellement corrige le .gitignore."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_SKILL_AUTO_ENROLLER_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-auto-enroller/SKILL.md
triggers:
  - "enroll skill"
  - "auto enroll"
  - "new skill"
  - "register skill pipeline"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - skill-auto-enroller

> **Verdict** : **SKILL D'EXECUTION** - Pipeline automatise d'enrolement de skill.

---

## Objectif

Executer les etapes 1-6 d Automated Citizenship en une seule commande.

---

## Declencheur

- Creation d'un nouveau skill dans `.kilo/skills/<repo>/`
- Ajout d'un skill externe dans un repo citoyen
- Synchronisation complete apres ajout manuel

---

## Etapes

| Etape | Action | Depend |
|-------|--------|--------|
| 1 | Verifier le repo dans known_repositories.yaml | - |
| 2 | Creer le verse dans VERSES/verses/ | Etape 1 |
| 3 | Enregistrer le citizen dans citizens.yaml | Etape 1 |
| 4 | Creer le bridge dans TOPOS/BRIDGES.yaml | Etape 1 |
| 5 | Inscrire le skill dans SKILLS/REGISTRY.yaml | Etape 1 |
| 6 | Mettre a jour .gitignore si necessaire | Etape 5 |

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `skill_name` | str | Nom du skill |
 | `repo_name` | str | Nom du repo |
 | `layer` | str | Couche logique (L0-L5) |
 | `local_path` | Path | Chemin local du repo |
 | `source_path` | str | Chemin source relatif du skill |
 | `update_gitignore` | bool | Si True, corrige le .gitignore |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `pipeline_report` | dict | Rapport d'execution |
 | `errors` | list | Erreurs critiques |
 | `warnings` | list | Avertissements |

---

## Regles

1. Chaque etape est atomique et tracee dans WAL
2. En cas d'echec, rollback automatique des etapes precedentes
3. Post-validation : executer probes P-801..P-907
4. Le skill doit etre enregistre dans REGISTRY.yaml avec source_repo

---

## Exemple d'usage

```python
from pathlib import Path
from skill_auto_enroller import SkillAutoEnroller

enroller = SkillAutoEnroller(
    known_repositories_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB/known_repositories.yaml"),
    citizens_yaml_path=Path("act-protocol/citizens.yaml"),
    verses_dir=Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/verses/"),
    bridges_path=Path("D:/DO/WEB/TOOLS/L1-INFRA/TOPOS/BRIDGES.yaml"),
    registry_yaml_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
    skills_dir=Path(".kilo/skills"),
)

report = enroller.enroll(
    skill_name="my-new-skill",
    repo_name="GeriCode",
    layer="L4",
    local_path=Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode"),
    source_path=".kilo/skills/my-new-skill/SKILL.md",
)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_enroll_new_skill` | Enrolement complet | Toutes etapes reussies |
 | `test_enroll_duplicate_skill` | Skill existant | Erreur P-806 |
 | `test_enroll_missing_repo` | Repo inconnu | Erreur P-801 |
 | `test_rollback_on_failure` | Echec etape 3 | Rollback etapes 1-2 |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-901    REGISTRY.yaml et registry.json synchronises                         |
 | P-902    citizens.yaml enrichi                                              |
 | P-903    100% skills ont frontmatter valide                                 |
 | P-904    0 doublon nom                                                     |
 | P-905    0 bridge orphelin                                                  |
 | P-906    0 cycle                                                           |
 | P-907    REGISTRY.yaml a source_repo pour skills externes                  |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          skill-auto-enroller fonctionne                                   |
 | [OK]          Toutes probes P-901..P-907 passent                               |
 | [OK]          Pipeline atomique avec rollback                                  |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `repo-citizen-manager`
 - `registry-sync`
 - `citizenship-auditor`
 - `bridge-auditor`
