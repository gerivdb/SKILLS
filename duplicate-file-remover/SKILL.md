---
name: duplicate-file-remover
description: Détecte et supprime les fichiers en double (même contenu, même hash) dans L4-TOOLS\SKILLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX. Utilise ce skill quand tu dois dédupliquer l'arborescence après copies, merges ou worktrees.
version: 1.0.0
intent_hash: 0xSKILL_DUPLICATE_FILE_REMOVER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/duplicate-file-remover/SKILL.md
---

# Skill — duplicate-file-remover

## Objectif

Maintenir l'intégrité du stockage en détectant les fichiers en double (identiques par contenu SHA-256) et en supprimant les copies redondantes, en conservant toujours une version canonique.

## Déclencheur

- Après création de worktree ou copie de répertoire
- Après merge de branches avec fichiers dupliqués
- Audit mensuel de l'espace disque
- Quand `duplicate`, `copy`, `backup` apparaissent dans les noms de fichiers

## Prérequis

- Accès en lecture et écriture aux répertoires cibles
- PowerShell 5.1+ ou certutil / sha256sum
- Espace disque suffisant pour le calcul des hash

## Protocole

### Étape 1 — Candidat au doublon (même taille)

```powershell
Get-ChildItem -Path <repo> -Recurse -File | 
  Group-Object Length | 
  Where-Object { $_.Count -gt 1 } | 
  Select-Object Name, Count
```

### Étape 2 — Vérification par hash SHA-256

Pour chaque groupe de fichiers de même taille, calculer le hash SHA-256 et identifier les vrais doublons :

```powershell
Get-FileHash -Path <chemin> -Algorithm SHA256
```

### Étape 3 — Détermination de la version canonique

Conserver le fichier situé dans le chemin le plus court ou le plus ancien (date de création), supprimer les autres.

| Critère | Priorité |
|---------|----------|
| Chemin le plus court | 1 |
| Date de création la plus ancienne | 2 |
| Ordre alphabétique | 3 |

### Étape 4 — Suppression des doublons

```powershell
Remove-Item -Path "<chemin_dupliqué>" -Force
```

### Étape 5 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "duplicate_file_remover_purge",
  "intent_hash": "0xSKILL_DUPLICATE_FILE_REMOVER_20261105",
  "data": {
    "duplicates_found": 12,
    "duplicates_removed": [
      {"hash": "a1b2c3...", "removed": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\copy\file.txt", "kept": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\file.txt"}
    ],
    "total_size_freed_mb": 15.3,
    "wal_logged": true
  }
}
```

## Règles de nettoyage

1. **Dry-run par défaut** : lister les doublons avant suppression
2. **Jamais supprimer** un fichier sans hash vérifié
3. **Conserver** la version canonique (chemin le plus court / plus ancien)
4. **Ne pas supprimer** les fichiers dans `.git/`, `.kilo/`, `node_modules/`
5. **Confirmation HITL** si un doublon se trouve dans un répertoire protégé

## Sortie standard

```yaml
files_scanned: 1250
duplicate_groups_found: 8
duplicates_removed: []
canonical_kept: []
total_size_freed_mb: 0
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Supprimer un fichier sans vérifier le hash SHA-256
- Supprimer dans `.git/`, `.kilo/`, `node_modules/`
- Ne pas conserver de version canonique
- Négliger le logging WAL après purge

## Intégration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/dedup-files.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-DUPLICATE_FILE_HYGIENE
- **IntentHash** : 0xSKILL_DUPLICATE_FILE_REMOVER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed