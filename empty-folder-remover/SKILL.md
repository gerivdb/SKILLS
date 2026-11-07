---
name: empty-folder-remover
description: Détecte et supprime les dossiers vides orphelins dans L4-TOOLS\SKILLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX. Utilise ce skill quand tu dois ranger l'arborescence après suppression de fichiers ou de skills.
version: 1.0.0
intent_hash: 0xSKILL_EMPTY_FOLDER_REMOVER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/empty-folder-remover/SKILL.md
---

# Skill — empty-folder-remover

## Objectif

Maintenir une arborescence propre en détectant et supprimant les dossiers vides qui subsistent après la suppression de fichiers, de skills ou de worktrees, sans toucher aux dossiers système protégés (`.git`, `.kilo`, `node_modules`, etc.).

## Déclencheur

- Après suppression d'un skill ou d'un fichier
- Après fusion ou déplacement de worktree
- Audit hebdomadaire de l'arborescence
- Avant archivage ou transfert de repo

## Prérequis

- Accès en écriture aux répertoires cibles
- PowerShell 5.1+ ou Bash
- Liste des dossiers protégés (ne jamais supprimer)

## Dossiers protégés (jamais supprimer)

| Dossier | Raison |
|---------|--------|
| `.git` | Contrôle de version |
| `.kilo` | Harness Agent Manager |
| `node_modules` | Dépendances JS/Bun |
| `.pytest_cache` | Cache de tests |
| `.ruff_cache` | Cache Ruff |
| `.benchmarks` | Données de benchmark |
| `.swarm` | Données swarm |
| `__pycache__` | Cache Python (géré par cache-cleaner) |
| `.vscode` | Configuration IDE |
| `.github` | CI/CD |

## Protocole

### Étape 1 — Détection des dossiers vides

```powershell
# Récursivement, trouver les dossiers sans contenu (sauf fichiers cachés protégés)
Get-ChildItem -Path <repo> -Recurse -Directory | 
  Where-Object { 
    $_.GetFileSystemInfos().Count -eq 0 -or 
    ($_.GetFileSystemInfos() | Where-Object { $_.Name -notmatch '^\.' }).Count -eq 0 
  } |
  Select-Object FullName
```

### Étape 2 — Vérification de protection

Exclure tous les dossiers de la liste protégée ci-dessus. Ne jamais supprimer un dossier contenant un fichier `.gitkeep`.

### Étape 3 — Suppression

```powershell
Remove-Item -Path "<chemin>\dossier_vide" -Force
```

### Étape 4 — Récursion

Après suppression, réexécuter la détection car de nouveaux dossiers vides peuvent apparaître (dossiers parents devenus vides).

### Étape 5 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "empty_folder_remover_purge",
  "intent_hash": "0xSKILL_EMPTY_FOLDER_REMOVER_20261105",
  "data": {
    "folders_removed": [
      {"path": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\old-skill\empty_subdir"}
    ],
    "total_removed": 1,
    "wal_logged": true
  }
}
```

## Règles de nettoyage

1. **Dry-run par défaut** : lister les dossiers vides avant suppression
2. **Récursif** : répéter jusqu'à ce qu'aucun dossier vide ne reste
3. **Ne jamais supprimer** un dossier protégé ou contenant `.gitkeep`
4. **Ne jamais supprimer** la racine du repo
5. **Ne jamais supprimer** un dossier contenant des fichiers cachés non protégés sans confirmation

## Sortie standard

```yaml
folders_scanned: 234
folders_empty_found: 5
folders_removed: []
folders_protected: []
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Supprimer `.git` ou `node_modules`
- Supprimer un dossier contenant `.gitkeep`
- Ne pas récurser après suppression (dossiers parents orphelins)
- Négliger le logging WAL après purge

## Intégration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/cleanup-empty-folders.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-EMPTY_FOLDER_HYGIENE
- **IntentHash** : 0xSKILL_EMPTY_FOLDER_REMOVER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed