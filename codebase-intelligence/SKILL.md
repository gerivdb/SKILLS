---
name: codebase-intelligence
description: >
  Orchestration de ecosystem-brain + codebase-memory-mcp pour des réponses
  combinées sur l'écosystème GeriCode. Répond à la fois à "où est X" et
  "que fait X / comment X est implémenté".
  Utiliser pour toute question nécessitant à la fois découverte structurelle
  et intelligence sémantique du code.
version: "1.0.0"
status: active
intent_hash: 0xCODEBASE_INTELLIGENCE_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/codebase-intelligence/SKILL.md
triggers:
  - "codebase memory"
  - "intelligence codebase"
  - "où est"
  - "que fait"
  - "comment est implémenté"
  - "recherche sémantique"
  - "cross-repo"
  - "N243"
tools:
  - bash
  - read
  - grep
citizen: "PRIMUS"
layer: "L4"
---

# Skill — Codebase Intelligence

> **Verdict** : **SKILL D'EXÉCUTION** — Orchestration de `ecosystem-brain`
> + `codebase-memory-mcp` pour des réponses combinées.

---

## Objectif

Combiner :
- **Découverte structurelle** (`ecosystem-brain`) : où sont les fichiers, designs, MCP, workflows
- **Intelligence sémantique** (`codebase-memory-mcp`) : que fait ce code, comment est-il implémenté

Pour répondre à des questions complexes comme :
- “Où est le endpoint MCP `git` et comment fonctionne-t-il ?”
- “Quels skills gèrent les MCP et que font-ils exactement ?”
- “Montre-moi tous les chemins Python dans `mcp.json` et leur rôle”

---

## Architecture

```
┌─────────────────────────────────────────────┐
│           Question utilisateur               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              codebase-intelligence           │
│  ┌─────────────────┐  ┌──────────────────┐  │
│  │ ecosystem-brain  │  │ codebase-memory  │  │
│  │  (structure)     │  │      -mcp        │  │
│  │  "OÙ EST X ?"    │  │  "QUE FAIT X ?"  │  │
│  └─────────────────┘  └──────────────────┘  │
│                    │                         │
│                    ▼                         │
│            ┌─────────────────┐              │
│            │  Fusion réponses │              │
│            └─────────────────┘              │
└─────────────────────────────────────────────┘
```

---

## Processus

### Étape 1 — Analyser la question

| Type de question | Couche à interroger |
|------------------|---------------------|
| “Où est X ?” / “Quel chemin ?” | `ecosystem-brain` |
| “Que fait X ?” / “Comment ?” | `codebase-memory-mcp` |
| “Cross-repo” / “N243” | Les deux |
| “MCP” / “Skill” | Les deux |

### Étape 2 — Découvrir la structure

```powershell
# Via ecosystem-brain / index-ecosystem.py
python .kilo/scripts/index-ecosystem.py --query "<terme>"
```

Résultat : chemins, types, strata, source_path.

### Étape 3 — Comprendre le code

```powershell
# Via codebase-memory-mcp (déjà installé et déclaré)
# Interrogation sémantique de la base de code
```

Résultat : explication, implémentation, dépendances.

### Étape 4 — Fusionner

Combiner :
- Les chemins et métadonnées de `ecosystem-brain`
- Les explications sémantiques de `codebase-memory-mcp`

Livrable : réponse unifiée.

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `PRIMUS` | Orchestre la combinaison des deux couches |
| `NEXUS` | Trace les requêtes et réponses dans WAL |
| `ARGUS` | Détecte les incohérences entre structure et sémantique |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1301   ecosystem-index.json existe et est à jour                          |
| P-1302   codebase-memory-mcp est déclaré et installé                       |
| P-1303   Toutes les requêtes --query retournent des résultats               |
| P-1304   Les chemins trouvés dans l'index correspondent aux fichiers réels  |
| P-1305   Les réponses sémantiques sont cohérentes avec la structure          |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          ecosystem-brain opérationnel                                     |
| ✓          codebase-memory-mcp opérationnel                                 |
| ✓          Réponses combinées structure + sémantique                        |
| ✓          Zéro incohérence entre index et code réel                        |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Débrancher `codebase-memory-mcp` de `mcp.json`.
2. Revenir à `ecosystem-brain` seul.
3. Logger dans WAL.
4. Corriger via PR review PRIMUS.

---

## Références

- `.kilo/skills/ecosystem-brain/SKILL.md`
- `.kilo/skills/mcp-guardian/SKILL.md`
- `.kilo/scripts/index-ecosystem.py`
- `ecosystem-index.json`
- `C:\DevTools\.kilocode\mcp.json`
- `C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe`
