---
name: progress-sync
description: "Synchronise automatiquement les sections d'etat des PRD MOC avec la realite des livrables et l'execution des probes. Remplace la mise a jour manuelle par un mecanisme auto-descriptif."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_PROGRESS_SYNC_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/progress-sync/SKILL.md
triggers:
  - "sync progression PRD MOC"
  - "que reste t il a faire"
  - "progress sync"
  - "BOOT-5B"
tools:
  - read
  - write
  - bash
citizen: "ECOSYSTEM-BRAIN"
layer: "L4"
---

# Skill - Progress Sync

> **Verdict** : **SKILL D'EXECUTION** - Synchronisation automatique des PRD MOC.

## Objectif

Lire les PRD MOC, verifier l'existence des livrables, executer les probes,
et mettre a jour les sections d'etat et "Reste a faire" automatiquement.

## Declencheur

- Boot de session (`BOOT-5B`)
- Post-commit sur livrable liste dans un PRD MOC
- Post-execution de probe P-7xx/P-8xx
- Demande utilisateur "que reste-t-il a faire ?"

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `prd_moc_paths` | list | Chemins des PRD MOC a synchroniser |
| `skills_registry` | Path | Chemin vers `SKILLS/REGISTRY.yaml` |
| `probe_runner` | string | `pytest` / `behave` / `custom` |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `updated_prd_mocs` | list | PRD MOC modifies avec changements |
| `report` | object | Resume: total, updated, unchanged, errors |

## Algorithme

```
1. Pour chaque PRD MOC :
   a. Parser frontmatter + sections
   b. Extraire tableau "Etat d'avancement"
   c. Extraire section "Reste a faire"
   d. Extraire bloc progress_tracking
   e. Verifier chaque livrable
   f. Executer probes si definies
   g. Mettre a jour statuts
   h. Reecrire uniquement si changements
2. Generer rapport
```

## Statuts autorises

- `[OK] FAIT`
- `[WIP] EN COURS`
- `[WIP] A FAIRE`
- `[KO] BLOQUE`

## Regles

1. Section `## Etat d'avancement` = source de verite
2. Section `## Reste a faire` = derivee des statuts [WIP] A FAIRE et [KO] BLOQUE
3. Bloc `progress_tracking` = obligatoire
4. Mise a jour atomique = un seul commit par PRD MOC
5. Aucun PRD MOC sans `progress_tracking` n'est valide
