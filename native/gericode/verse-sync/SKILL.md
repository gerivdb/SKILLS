---
name: verse-sync
description: "Synchronise VERSES/verses/ <-> ONTOLOGY/glossary.yaml <-> TQL."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_VERSE_SYNC_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/verse-sync/SKILL.md
triggers:
  - "sync verses"
  - "verse ontology sync"
  - "tql sync"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - verse-sync

> **Verdict** : **SKILL D'EXECUTION** - Synchronise les verses avec l'ontologie.

---

## Objectif

Garantir la coherence entre VERSES/verses/, ONTOLOGY/glossary.yaml et TQL.

---

## Declencheur

- Nouveau concept dans ONTOLOGY
- Nouveau verse dans VERSES
- Modification TQL

---

## Entrees

 | Entree | Type | Description |
 |--------|------|-------------|
 | `verses_dir` | Path | Repertoire VERSES/verses/ |
 | `ontology_path` | Path | Chemin vers ONTOLOGY/glossary.yaml |
 | `tql_path` | Path | Chemin vers TQL (optionnel) |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `sync_report` | dict | Rapport de synchronisation |
 | `missing_verses` | list | Concepts sans verse |
 | `missing_concepts` | list | Verses sans concept |

---

## Regles

1. Tout concept dans ONTOLOGY doit avoir un verse
2. Tout verse doit referencer un concept ontologique
3. TQL peut requeter tous les concepts

---

## Exemple d'usage

```python
from pathlib import Path
from verse_sync import VerseSync

sync = VerseSync(
    verses_dir=Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES/verses/"),
    ontology_path=Path("D:/DO/WEB/TOOLS/L0-CANON/ONTOLOGY/ONTOLOGY/glossary.yaml"),
)
report = sync.sync(dry_run=False)
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_sync_missing_verse` | Concept sans verse | Detecte |
 | `test_sync_missing_concept` | Verse sans concept | Detecte |
 | `test_sync_complete` | Synchronisation complete | 0 missing |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-916    100% concepts ontologiques ont un verse                           |
 | P-917    100% repo-citizen verses referencent un repo connu                 |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Criteres

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITERE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | [OK]          verse-sync fonctionne                                            |
 | [OK]          P-916 passe                                                      |
 | [OK]          P-917 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## References

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `VERSES/verses/`
 - `ONTOLOGY/glossary.yaml`
