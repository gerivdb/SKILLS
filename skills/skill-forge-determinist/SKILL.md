---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SFD_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/skill-forge-determinist/SKILL.md
---

# Skill — skill-forge-determinist

## Objectif

Scaffolder unitaire : créer un skill L4 en une transaction atomique (template `SKILL.md`, script en encodage CP1252 strict, entrées `REGISTRY.yaml` et `MANIFEST.json`, jonctions NTFS). Divise par 20 le temps de création d'une compétence. Couche Méta-Skills & Cycle de Vie.

## Déclencheur

- Création d'un nouveau skill L4 dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/`
- Demande de scaffolding d'une compétence déterministe

## Entrées

- `skill_name`: nom du skill à créer (format kebab-case)
- `skill_description`: description fonctionnelle courte
- `skill_triggers`: liste des déclencheurs (optionnel)
- `target_repo`: chemin du dépôt cible (défaut : `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS`)

## Sorties

- Dossier du skill créé avec `SKILL.md` et `scripts/`
- Entrée ajoutée dans `REGISTRY.yaml` et `MANIFEST.json`
- Jonctions NTFS créées vers `.kilocode\skills\` et `.gemini\config\skills\`
- Entrée WAL NEXUS horodatée

## Règles

### 1. Transaction atomique

Toute création de skill est une transaction : si une étape échoue, tout est annulé (rollback). Pas de skill partiellement créé.

### 2. Encodage CP1252 strict

Tous les scripts PowerShell doivent être en encodage CP1252 sans caractères Unicode spéciaux (émojis, tirets longs, etc.).

### 3. Frontmatter YAML standardisé

Chaque `SKILL.md` doit contenir :
- `type: SKILL`
- `version`, `status`, `date`, `intent_hash`
- `layer: L4-TOOLS`
- `author`, `source_repo`, `source_path`

### 4. Section WAL NEXUS

Chaque `SKILL.md` doit inclure une section `## WAL NEXUS` pour tracer les interventions.

## Script d'investigation

`scripts/forge.ps1` — voir ci-dessous.

## Tests

- `tests/test_skill_forge_determinist.ps1` — créer un skill factice, vérifier la présence de `SKILL.md`, `scripts/`, l'entrée dans `REGISTRY.yaml`.

## Probes

- Chaque skill créé possède un `SKILL.md` avec frontmatter valide
- Chaque skill créé possède un dossier `scripts/` avec au moins un script
- L'entrée `REGISTRY.yaml` est présente pour chaque skill créé

## WAL NEXUS

```
[WAL_NEXUS] skill=skill-forge-determinist action=forge timestamp=<ISO> skill_name=<NAME> repo=<REPO> status=<OK|FAIL>
[WAL_NEXUS] skill=skill-forge-determinist action=rollback timestamp=<ISO> skill_name=<NAME> reason=<motif>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
