---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_YAML_SAFE_INJECTOR_20260807
---

# Skill - yaml-safe-injector

## Objectif

Injecter des champs dans un YAML complexe sans corrompre la structure.
Preserve quoted strings multiline, ancres YAML, commentaires, ordre des cles.

## Declencheur

- Toute ecriture dans `known_repositories.yaml` ou autre SOT YAML
- Injection de `verse_mapping` ou metadonnees N243
- Modification de registres YAML complexes

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `target_path` | Path | Chemin du fichier YAML cible |
| `updates` | dict | Champs a injecter/mettre a jour |
| `dry_run` | bool | Si True, simulation sans ecriture |
| `create_backup` | bool | Si True, backup .bak automatique |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `target_path` | Path | Chemin du fichier modifie |
| `diff` | str | Diff unifie des changements |

## Regles

### 1. Toujours utiliser ruamel.yaml
- `preserve_quotes = True` pour garder les quoted strings
- `width = 4096` pour eviter les coupures de ligne
- Pas d'autres bibliotheques YAML (PyYAML corrompt les structures complexes)

### 2. Backup automatique
- Extension `.bak` ajoutee avant toute ecriture
- Rollback automatique si validation post-ecriture echoue

### 3. Validation stricte
- Parse YAML avant ecriture
- Re-parse apres ecriture pour verifier l'integrite
- Rollback si la validation echoue

### 4. Diff minimal
- Utiliser `difflib.unified_diff` pour le diff
- Le diff montre exactement ce qui change

## Exemple d'usage

```python
from pathlib import Path
from yaml_safe_injector import inject_yaml

target = Path("known_repositories.yaml")
updates = {
    "P0_REPOS": [
        {
            "name": "NEW-REPO",
            "local_path": "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\NEW-REPO",
            "layer": "L4",
        }
    ]
}

path, diff = inject_yaml(target, updates, dry_run=True)
print(diff)

# Si le diff est acceptable :
path, diff = inject_yaml(target, updates)
```

## Tests

| Test | Description |
|------|-------------|
| `test_inject_new_key` | Ajoute une cle racine |
| `test_inject_nested_key` | Ajoute une cle dans un mapping imbrique |
| `test_preserve_quotes` | Preserve les quoted strings multiline |
| `test_preserve_anchors` | Preserve les ancres YAML |
| `test_dry_run` | dry_run ne modifie pas le fichier |
| `test_rollback_on_corruption` | Rollback si validation post-ecriture echoue |
| `test_backup_created` | Backup .bak cree et supprime apres succes |

## Reference ADR

- **ADR** : ADR-2026-08-07-001-YAML-SAFE-INJECTOR
- **IntentHash** : 0xADR_YAML_SAFE_INJECTOR_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
