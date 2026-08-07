---
name: ecosystem-brain
description: >
  Systeme de decouverte automatique de l'ecosysteme GeriCode.
  Scanne designs, skills, citizens, workflows, MCP et personae pour construire
  un index unifie interrogeable. Reduit la surcharge cognitive en eliminant
  la recherche manuelle.
  Utiliser pour toute action necessitant de decouvrir des elements de l'ecosysteme.
version: "1.0.0"
status: active
intent_hash: 0xECOSYSTEM_BRAIN_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ecosystem-brain/SKILL.md
triggers:
  - "decouvrir"
  - "rechercher element"
  - "index ecosystem"
  - "quel skill"
  - "quel citizen"
  - "design pour"
tools:
  - bash
  - read
  - grep
citizen: "PRIMUS"
layer: "L4"
---

# Skill - Ecosystem Brain

> **Verdict** : **SKILL D'EXECUTION** - Systeme de decouverte automatique
> de l'ecosysteme pour eliminer la surcharge cognitive.

---

## Objectif

Scanne automatiquement tous les elements de l'ecosysteme et construit un index unifie interrogeable.

---

## Processus

### Etape 1 - Decouvrir

```powershell
# Lancer le scan complet
python .kilo/scripts/index-ecosystem.py --scan-all
```

### Etape 2 - Requeter

```powershell
# Rechercher un element
python .kilo/scripts/index-ecosystem.py --query "nomenclature PRD-MOC"

# Rechercher un skill
python .kilo/scripts/index-ecosystem.py --query "skill verify-terms"

# Rechercher un citizen
python .kilo/scripts/index-ecosystem.py --query "citizen MOX"
```

### Etape 3 - Executer

```powershell
# Obtenir le plan d'execution
python .kilo/scripts/index-ecosystem.py --plan "renommer PRD-MOC-N243"
```

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `PRIMUS` | Orchestre la decouverte et l'execution |
| `NEXUS` | Trace les evenements dans WAL |
| `ARGUS` | Detecte les gaps dans l'index |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1101   ecosystem-index.json existe et est a jour                          |
| P-1102   Tous les designs sont decouverts                                   |
| P-1103   Tous les skills sont decouverts                                    |
| P-1104   Tous les citizens sont decouverts                                  |
| P-1105   Tous les workflows sont decouverts                                 |
| P-1106   Tous les MCP sont decouverts                                       |
| P-1107   Tous les personae sont decouverts                                  |
| P-1108   IntentHash unique pour chaque element                              |
| P-1109   WAL trace toutes les actions                                       |
| P-1110   Topologie globalisante disponible                                  |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          ecosystem-index.json present et complet                          |
| [OK]          Tous les elements decouverts sans manque                         |
| [OK]          Causalite tracee pour chaque action                              |
| [OK]          Topologie globalisante disponible                                |
| [OK]          Zero element orphelin                                            |
| [OK]          Zero duplication non detectee                                    |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `ecosystem-index.json`.
2. Revenir a l'index precedent.
3. Logger dans WAL.
4. Corriger via PR review ARGUS.

---

## References

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `unified-design/designs/aep-fractal-repo-structure.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `citizens.yaml`
- `ONTOLOGY_DECLARATION.yaml`
- `.kilo/skills/*/SKILL.md`
- `.github/workflows/nomenclature-guard.yml`
- `mcp.json`
