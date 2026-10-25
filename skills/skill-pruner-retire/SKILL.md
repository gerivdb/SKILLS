---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SPR_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/skill-pruner-retire/SKILL.md
---

# Skill — skill-pruner-retire

## Objectif

Décommissionne proprement un skill ou un Combo obsolète : retrait sécurisé des jonctions NTFS, archivage, nettoyage des registres (REGISTRY.yaml, MANIFEST.json). Empêche l'accumulation de code mort dans L4-TOOLS. Couche Méta-Skills & Cycle de Vie.

## Déclencheur

- Un skill n'est plus utilisé par aucun Combo
- Un skill est remplacé par une version plus récente
- Un skill génère des erreurs récurrentes (détecté par skill-linter-sentinel)

## Entrées

- `skill_name`: nom du skill à retirer
- `archive`: déplacer vers un dossier d'archivage au lieu de supprimer (défaut : true)
- `clean_registry`: retirer l'entrée de REGISTRY.yaml et MANIFEST.json (défaut : true)
- `clean_junctions`: retirer les jonctions NTFS (défaut : true)

## Sorties

- Skill archivé ou supprimé
- Entrées retirées de REGISTRY.yaml et MANIFEST.json
- Jonctions NTFS supprimées
- Entrée WAL NEXUS horodatée

## Règles

### 1. Vérification avant retrait

Avant de retirer un skill, vérifier qu'il n'est pas référencé par un Combo actif (via skill-synapse-weaver).

### 2. Archivage plutôt que suppression

Par défaut, le skill est déplacé vers un dossier d'archivage (`D:\DO\WEB\TOOLS\L5-ARCHIVE\skills\`) plutôt que supprimé définitivement.

### 3. Nettoyage des jonctions NTFS

Les jonctions vers `.kilocode\skills\` et `.gemini\config\skills\` doivent être supprimées.

### 4. Transaction atomique

Toute opération de retrait est atomique : si une étape échoue, tout est annulé.

## Script d'investigation

`scripts/prune.ps1` — voir ci-dessous.

## Tests

- `tests/test_skill_pruner_retire.ps1` — créer un skill factice, le retirer, vérifier qu'il n'y a plus de référence.

## Probes

- Zéro référence à un skill retiré dans REGISTRY.yaml
- Zéro jonction orpheline après retrait
- Skill retiré présent dans l'archive (si archive = true)

## WAL NEXUS

```
[WAL_NEXUS] skill=skill-pruner-retire action=prune timestamp=<ISO> skill_name=<NAME> archived=<bool> status=<OK|FAIL>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
