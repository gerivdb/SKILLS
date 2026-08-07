---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_YAML_SAFE_INJECTOR_20260807
---

# Skill — yaml-safe-injector

## Objectif

Injecter des champs dans un YAML complexe sans corrompre la structure.
Préserve quoted strings multiline, ancres YAML, commentaires, ordre des clés.

## Déclencheur

- Toute écriture dans `known_repositories.yaml` ou autre SOT YAML
- Injection de `verse_mapping` ou métadonnées N243
- Modification de registres YAML complexes

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `target_path` | Path | Chemin du fichier YAML cible |
| `updates` | dict | Champs à injecter/mettre à jour |
| `dry_run` | bool | Si True, simulation sans écriture |
| `create_backup` | bool | Si True, backup .bak automatique |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `target_path` | Path | Chemin du fichier modifié |
| `diff` | str | Diff unifié des changements |

## Règles

### 1. Toujours utiliser ruamel.yaml
- `preserve_quotes = True` pour garder les quoted strings
- `width = 4096` pour éviter les coupures de ligne
- Pas d'autres bibliothèques YAML (PyYAML corrompt les structures complexes)

### 2. Backup automatique
- Extension `.bak` ajoutée avant toute écriture
- Rollback automatique si validation post-écriture échoue

### 3. Validation stricte
- Parse YAML avant écriture
- Re-parse après écriture pour vérifier l'intégrité
- Rollback si la validation échoue

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
| `test_inject_new_key` | Ajoute une clé racine |
| `test_inject_nested_key` | Ajoute une clé dans un mapping imbriqué |
| `test_preserve_quotes` | Préserve les quoted strings multiline |
| `test_preserve_anchors` | Préserve les ancres YAML |
| `test_dry_run` | dry_run ne modifie pas le fichier |
| `test_rollback_on_corruption` | Rollback si validation post-écriture échoue |
| `test_backup_created` | Backup .bak créé et supprimé après succès |

## Référence ADR

- **ADR** : ADR-2026-08-07-001-YAML-SAFE-INJECTOR
- **IntentHash** : 0xADR_YAML_SAFE_INJECTOR_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
