---
name: log-rotator
description: Rotate et archive les fichiers de log anciens dans L4-TOOLS\SKILLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX. Utilise ce skill quand tu dois gérer la croissance des fichiers de log (.log, interception-log, test-output.log) et les archiver dans .kilo/logs/archive/.
version: 1.0.0
intent_hash: 0xSKILL_LOG_ROTATOR_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/log-rotator/SKILL.md
---

# Skill — log-rotator

## Objectif

Gérer la croissance des fichiers de log en les rotatant (compression + archivage) lorsqu'ils dépassent une taille ou un âge seuil, et en supprimant les logs trop anciens après archivage.

## Déclencheur

- Fichier de log > 10 Mo
- Fichier de log > 30 jours
- Audit hebdomadaire d'espace disque
- Avant archivage de worktree

## Prérequis

- Accès en écriture aux répertoires cibles
- Répertoire d'archive `.kilo/logs/archive/` existant
- PowerShell 5.1+ ou 7z / gzip pour compression

## Seuils de rotation

| Critère | Valeur | Action |
|---------|--------|--------|
| Taille max par log | 10 Mo | Rotation (archive + nouveau fichier) |
| Âge max par log | 30 jours | Archivage puis suppression |
| Taille totale des logs | 500 Mo | Alerte + rotation forcée |
| Nombre de rotations conservées | 10 | Suppression des plus anciennes |

## Protocole

### Étape 1 — Détection des logs à rotater

```powershell
Get-ChildItem -Path <repo> -Recurse -Filter *.log | 
  Where-Object { $_.Length -gt 10MB -or $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
  Select-Object FullName, Length, LastWriteTime
```

### Étape 2 — Archivage

Compresser le fichier log et le déplacer dans `.kilo/logs/archive/` avec timestamp :

```powershell
$archiveName = "{0}_{1:yyyyMMdd_HHmmss}.log.gz" -f $baseName, (Get-Date)
Compress-Archive -Path <log_file> -DestinationPath ".kilo/logs/archive/$archiveName"
```

### Étape 3 — Rotation

Créer un nouveau fichier de log vide ou vider l'existant après archivage.

### Étape 4 — Nettoyage des archives anciennes

Supprimer les archives de plus de 90 jours dans `.kilo/logs/archive/`.

### Étape 5 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "log_rotator_rotation",
  "intent_hash": "0xSKILL_LOG_ROTATOR_20261105",
  "data": {
    "logs_rotated": [
      {"name": "interception-log.txt", "size_mb": 22.5, "archived": true}
    ],
    "archives_cleaned": [],
    "total_size_freed_mb": 45.2,
    "wal_logged": true
  }
}
```

## Règles de rotation

1. **Dry-run par défaut** : lister les logs avant rotation
2. **Ne jamais supprimer** un log sans archivage préalable
3. **Ne jamais supprimer** un log ouvert par un processus actif
4. **Conserver** au minimum 3 rotations successives
5. **Alerte** si la taille totale des logs dépasse 500 Mo

## Sortie standard

```yaml
logs_scanned: 24
logs_rotated: []
archives_created: []
archives_cleaned: []
total_size_freed_mb: 0
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Supprimer un log sans archivage
- Rotater un log ouvert par un processus actif
- Négliger le nettoyage des archives (> 90 jours)
- Négliger le logging WAL après rotation

## Intégration

- **GeriCode** : `scripts/daily-maintenance.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/rotate-logs.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-LOG_ROTATION_MECHANISM
- **IntentHash** : 0xSKILL_LOG_ROTATOR_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed