---
name: ecosystem-brain
description: >
  Système de découverte automatique de l'écosystème GeriCode.
  Scanne designs, skills, citizens, workflows, MCP et personae pour construire
  un index unifié interrogeable. Réduit la surcharge cognitive en éliminant
  la recherche manuelle.
  Utiliser pour toute action nécessitant de découvrir des éléments de l'écosystème.
version: "1.0.0"
status: active
intent_hash: 0xECOSYSTEM_BRAIN_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ecosystem-brain/SKILL.md
triggers:
  - "découvrir"
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

# Skill — Ecosystem Brain

> **Verdict** : **SKILL D'EXÉCUTION** — Système de découverte automatique
> de l'écosystème pour éliminer la surcharge cognitive.

---

## Objectif

Scanne automatiquement tous les éléments de l'écosystème et construit un index unifié interrogeable.

---

## Processus

### Étape 1 — Découvrir

```powershell
# Lancer le scan complet
python .kilo/scripts/index-ecosystem.py --scan-all
```

### Étape 2 — Requêter

```powershell
# Rechercher un élément
python .kilo/scripts/index-ecosystem.py --query "nomenclature PRD-MOC"

# Rechercher un skill
python .kilo/scripts/index-ecosystem.py --query "skill verify-terms"

# Rechercher un citizen
python .kilo/scripts/index-ecosystem.py --query "citizen MOX"
```

### Étape 3 — Exécuter

```powershell
# Obtenir le plan d'exécution
python .kilo/scripts/index-ecosystem.py --plan "renommer PRD-MOC-N243"
```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `PRIMUS` | Orchestre la découverte et l'exécution |
| `NEXUS` | Trace les événements dans WAL |
| `ARGUS` | Détecte les gaps dans l'index |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1101   ecosystem-index.json existe et est à jour                          |
| P-1102   Tous les designs sont découverts                                   |
| P-1103   Tous les skills sont découverts                                    |
| P-1104   Tous les citizens sont découverts                                  |
| P-1105   Tous les workflows sont découverts                                 |
| P-1106   Tous les MCP sont découverts                                       |
| P-1107   Tous les personae sont découverts                                  |
| P-1108   IntentHash unique pour chaque élément                              |
| P-1109   WAL trace toutes les actions                                       |
| P-1110   Topologie globalisante disponible                                  |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          ecosystem-index.json présent et complet                          |
| ✓          Tous les éléments découverts sans manque                         |
| ✓          Causalité tracée pour chaque action                              |
| ✓          Topologie globalisante disponible                                |
| ✓          Zéro élément orphelin                                            |
| ✓          Zéro duplication non détectée                                    |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `ecosystem-index.json`.
2. Revenir à l'index précédent.
3. Logger dans WAL.
4. Corriger via PR review ARGUS.

---

## Références

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `unified-design/designs/aep-fractal-repo-structure.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `citizens.yaml`
- `ONTOLOGY_DECLARATION.yaml`
- `.kilo/skills/*/SKILL.md`
- `.github/workflows/nomenclature-guard.yml`
- `mcp.json`
