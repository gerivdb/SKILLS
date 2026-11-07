---
name: temp-file-cleaner
description: Nettoie les fichiers temporaires orphelins (.tmp, .log anciens, .obj, interception-log, test_output.log, etc.) dans L4-TOOLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX. Utilise ce skill quand tu dois libérer de l'espace disque ou ranger les artefacts de session.
version: 1.0.0
intent_hash: 0xSKILL_TEMP_FILE_CLEANER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/temp-file-cleaner/SKILL.md
---

# Skill — temp-file-cleaner

## Objectif

Maintenir la propreté du système de fichiers en détectant et supprimant les fichiers temporaires, logs anciens et artefacts de session qui s'accumulent dans les répertoires de développement.

## Déclencheur

- Fin de session KiloCode / Agent Manager
- Audit quotidien d'espace disque
- Après exécution de scripts Python ou PowerShell générant des logs
- Avant archivage d'un worktree
- Quand `.log`, `.tmp`, `.obj` dépassent un seuil configurable

## Prérequis

- Accès en écriture aux répertoires cibles
- PowerShell 5.1+ ou Bash
- Liste des extensions de fichiers temporaires à cibler

## Extensions et patterns de fichiers temporaires

| Pattern | Description | Âge max avant purge | Risque |
|---------|-------------|---------------------|--------|
| `*.tmp` | Fichiers temporaires génériques | 1 jour | Faible |
| `*.log` (ancien) | Logs de session > 7 jours | 7 jours | Faible |
| `interception-log.txt` | Logs d'interception LLM | 30 jours | Moyen |
| `*.obj` | Fichiers objets Python compilés | 7 jours | Faible |
| `trix-test-output.log` | Logs de test TRIX | 7 jours | Faible |
| `*test-output.log` | Logs de test génériques | 7 jours | Faible |
| `*.pyc` | Bytecode Python orphelin | 7 jours | Faible |
| `.DS_Store` | Métadonnées macOS | 1 jour | Faible |
| `Thumbs.db` | Miniatures Windows | 1 jour | Faible |

## Protocole

### Étape 1 — Détection des fichiers temporaires

```powershell
$cutoff = (Get-Date).AddDays(-7)
Get-ChildItem -Path <repo> -Recurse -File | 
  Where-Object { $_.Extension -in @('.tmp', '.log', '.obj') -and $_.LastWriteTime -lt $cutoff } |
  Select-Object FullName, Length, LastWriteTime
```

### Étape 2 — Vérification de protection

- Ne jamais supprimer un fichier `.log` ouvert par un processus actif
- Ne jamais supprimer `interception-log.txt` sans archivage préalable dans `.kilo/logs/`
- Vérifier qu'un fichier `.tmp` n'est pas verrouillé par une application

### Étape 3 — Suppression

```powershell
Remove-Item -Path "<chemin>\fichier.tmp" -Force
```

### Étape 4 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "temp_file_cleaner_purge",
  "intent_hash": "0xSKILL_TEMP_FILE_CLEANER_20261105",
  "data": {
    "files_purged": [
      {"name": "interception-log.txt", "path": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\interception-log.txt", "size_mb": 22.5}
    ],
    "total_size_freed_mb": 45.2,
    "wal_logged": true
  }
}
```

## Règles de nettoyage

1. **Dry-run par défaut** : lister avant suppression
2. **Âge minimum** : ne purger que les fichiers > 7 jours (sauf `*.tmp` > 1 jour)
3. **Ne jamais supprimer** un fichier verrouillé (erreur d'accès = skip)
4. **Archiver avant purge** : logs critiques → `.kilo/logs/archive/` avant suppression
5. **Seuil d'alerte** : signaler si un fichier temporaire dépasse 100 Mo

## Sortie standard

```yaml
files_scanned: 156
files_purged: []
files_kept: []
total_size_freed_mb: 0
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Supprimer `interception-log.txt` sans archivage
- Supprimer un fichier `.log` en cours d'écriture par un processus
- Utiliser `Remove-Item -Recurse -Force` sur des répertoires entiers sans filtre
- Négliger le logging WAL après purge

## Intégration

- **GeriCode** : `scripts/daily-maintenance.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/cleanup-temp.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-TEMP_FILE_HYGIENE
- **IntentHash** : 0xSKILL_TEMP_FILE_CLEANER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed