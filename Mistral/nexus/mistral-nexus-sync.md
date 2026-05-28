---
name: mistral-nexus-sync
strate: L1
source: Mistral
type: skill
description: Synchronisation des registres NEXUS via les outils Mistral (mcp_github, code_interpreter).
version: 1.0.0
date: 2026-05-28
author: JPEG Lubbin / Mistral AI
intent_hash: 0xSKILL_MISTRAL_NEXUS_SYNC_20260528
dependencies:
  - repo: gerivdb/NEXUS
  - tool: mcp_github
  - tool: code_interpreter
  - script: Mistral/scripts/mistral_nexus_sync.ps1
related_epics:
  - EPIC_MISTRAL_SKILLS_GOVERNANCE
related_prds:
  - PRD_MISTRAL_SKILLS_INTEGRATION
---

# Skill — Synchronisation NEXUS via Mistral

## Objectif
Automatiser la **synchronisation des registres NEXUS** (ex: `TritRegistry.yaml`, `OrgansRegistry.yaml`) entre le dépôt `gerivdb/NEXUS` et les dépôts locaux ou autres cibles, en utilisant les outils natifs de Mistral (`mcp_github`, `code_interpreter`).

## Contexte
- **Problème** : Les registres NEXUS (L1) doivent être **synchronisés manuellement** entre les dépôts, ce qui est source d'erreurs et de désynchronisation.
- **Solution** : Utiliser Mistral pour **automatiser** cette synchronisation via des appels API GitHub et des scripts PowerShell/Python.

## Prérequis
1. **Accès à `mcp_github`** : Permissions de lecture/écriture sur `gerivdb/NEXUS`.
2. **Dépôt local cloné** : `gerivdb/SKILLS` et `gerivdb/NEXUS` doivent être accessibles.
3. **Outils Mistral** : `code_interpreter` pour le traitement des données.

---

## Workflow

### 1. Récupération des Registres
**Action** : Récupérer les fichiers de registres depuis `gerivdb/NEXUS`.
**Outil** : `mcp_github.get_file_contents`
**Cible** :
- `gerivdb/NEXUS/TritRegistry.yaml`
- `gerivdb/NEXUS/OrgansRegistry.yaml`
- `gerivdb/NEXUS/known_repositories.yaml`

**Exemple de code** (via `code_interpreter`) :
```python
# Récupérer le contenu d'un registre
from github_app import get_file_contents

registre_content = get_file_contents(
    owner="gerivdb",
    repo="NEXUS",
    path="TritRegistry.yaml"
)
print(registre_content)
```

### 2. Comparaison avec les Registres Locaux
**Action** : Comparer les registres distants avec les versions locales (si elles existent).
**Outil** : `code_interpreter` (pour la comparaison des fichiers YAML).

**Exemple de code** :
```python
import yaml

# Charger les registres distants et locaux
remote_registry = yaml.safe_load(registre_content)
local_registry = yaml.safe_load(open("Mistral/nexus/TritRegistry.yaml"))

# Identifier les différences
differences = {
    "added": {k: v for k, v in remote_registry.items() if k not in local_registry},
    "removed": {k: v for k, v in local_registry.items() if k not in remote_registry},
    "modified": {}
}

for key in set(remote_registry.keys()) & set(local_registry.keys()):
    if remote_registry[key] != local_registry[key]:
        differences["modified"][key] = {
            "remote": remote_registry[key],
            "local": local_registry[key]
        }

print("Différences détectées :", differences)
```

### 3. Synchronisation
**Action** : Appliquer les modifications (création, mise à jour, suppression) sur les registres locaux.
**Outil** : `mcp_github.create_or_update_file` ou `mcp_github.delete_file`.

**Exemple de code** :
```python
# Mettre à jour un registre local
from github_app import create_or_update_file

create_or_update_file(
    owner="gerivdb",
    repo="SKILLS",
    path="Mistral/nexus/TritRegistry.yaml",
    content=yaml.dump(remote_registry),
    branch="feat/skills-mistral",
    message="Synchronisation de TritRegistry.yaml depuis NEXUS"
)
```

### 4. Validation
**Action** : Vérifier que les registres sont synchronisés et que les dépendances sont respectées.
**Outil** : `code_interpreter` (pour valider les schémas YAML).

**Exemple de code** :
```python
# Valider le schéma d'un registre
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "trits": {"type": "array"},
        "organs": {"type": "array"}
    },
    "required": ["trits"]
}

try:
    jsonschema.validate(instance=remote_registry, schema=schema)
    print("✅ Schéma valide")
except jsonschema.ValidationError as e:
    print(f"❌ Erreur de schéma : {e}")
```

---

## Exécution

### Via PowerShell (Recommandé)
Utiliser le script **`Mistral/scripts/mistral_nexus_sync.ps1`** :
```powershell
# Mode dry-run (simulation)
.\Mistral\scripts\mistral_nexus_sync.ps1 -DryRun

# Mode live (applique les modifications)
.\Mistral\scripts\mistral_nexus_sync.ps1 -Force
```

### Via Python (Alternative)
Utiliser `code_interpreter` pour exécuter les étapes manuellement.

---

## Sorties Attendues
| Type | Chemin | Description |
|------|--------|-------------|
| **Fichier** | `Mistral/nexus/TritRegistry.yaml` | Registre synchronisé. |
| **Fichier** | `Mistral/nexus/OrgansRegistry.yaml` | Registre synchronisé. |
| **Log** | `logs/mistral_nexus_sync_*.log` | Journal des opérations. |
| **Rapport** | `Mistral/nexus/sync_report_*.json` | Rapport des différences et actions. |

---

## Métriques de Succès
- **Taux de synchronisation** : 100% des registres NEXUS synchronisés sans erreur.
- **Temps d'exécution** : < 5 minutes pour une synchronisation complète.
- **Conformité** : 0 violation avec `rss_lint.py --strict`.

---

## Gestion des Erreurs
| Erreur | Cause | Solution |
|--------|-------|----------|
| **404 Not Found** | Fichier introuvable dans `gerivdb/NEXUS`. | Vérifier le chemin ou créer le fichier manquant. |
| **403 Forbidden** | Permissions insuffisantes. | Vérifier les droits d'accès à `gerivdb/NEXUS`. |
| **Conflit de fusion** | Différences non résolues. | Utiliser `-Force` ou résoudre manuellement. |
| **Schéma invalide** | Registre non conforme. | Corriger le fichier source dans `gerivdb/NEXUS`. |

---

## Dépendances
- **Dépôts** :
  - `gerivdb/NEXUS` (source des registres).
  - `gerivdb/SKILLS` (cible des synchronisations).
- **Outils** :
  - `mcp_github` (accès GitHub).
  - `code_interpreter` (traitement des données).
- **Scripts** :
  - `Mistral/scripts/mistral_nexus_sync.ps1` (automatisation).

---

## Notes
- **Mode Dry-Run** : Toujours tester en mode simulation (`-DryRun`) avant d'appliquer les modifications.
- **Logs** : Les logs sont stockés dans `logs/mistral_nexus_sync_*.log`.
- **Intégration CI** : Ce skill peut être intégré dans un pipeline KIVA pour une exécution automatique.

---
*IntentHash: 0xSKILL_MISTRAL_NEXUS_SYNC_20260528 | Version: 1.0.0 | Statut: DRAFT*