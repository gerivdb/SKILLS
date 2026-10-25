---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SLS_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/skill-linter-sentinel/SKILL.md
---

# Skill — skill-linter-sentinel

## Objectif

Linter continu : audite l'encodage (anti-Unicode non-CP1252), teste la validité `ast.parse` des scripts Python et la syntaxe PowerShell. Maintient la conformité pre-commit à 100%. Couche Méta-Skills & Cycle de Vie.

## Déclencheur

- Avant tout commit de skill L4
- Lors d'un audit de conformité des skills existants

## Entrées

- `skill_path`: chemin du skill à auditer (défaut : répertoire courant)
- `check_encoding`: vérifier l'encodage CP1252 (défaut : true)
- `check_python`: valider la syntaxe Python (défaut : true)
- `check_powershell`: valider la syntaxe PowerShell (défaut : true)

## Sorties

- Rapport JSON des erreurs et avertissements détectés
- Liste des fichiers non conformes
- Entrée WAL NEXUS horodatée

## Règles

### 1. Encodage CP1252

Tous les fichiers .ps1 doivent être encodés en CP1252 sans caractères Unicode spéciaux (émojis, tirets longs, etc.).

### 2. Syntaxe Python

Tous les fichiers .py doivent passer `py_compile` sans erreur.

### 3. Syntaxe PowerShell

Tous les fichiers .ps1 doivent passer `[System.Management.Automation.Language.Parser]::ParseFile()` sans erreur.

### 4. Frontmatter YAML

Chaque SKILL.md doit avoir un frontmatter YAML valide avec les champs obligatoires.

## Script d'investigation

`scripts/lint.ps1` — voir ci-dessous.

## Tests

- `tests/test_skill_linter_sentinel.ps1` — créer des fichiers non conformes, vérifier qu'ils sont détectés.

## Probes

- Zéro fichier .ps1 avec caractères Unicode non-CP1252
- Zéro fichier .py avec erreur de syntaxe
- Zéro fichier .ps1 avec erreur de parsing PowerShell

## WAL NEXUS

```
[WAL_NEXUS] skill=skill-linter-sentinel action=lint timestamp=<ISO> path=<PATH> errors=<n> warnings=<m> status=<OK|FAIL>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
