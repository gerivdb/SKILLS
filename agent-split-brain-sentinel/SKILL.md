---
name: agent-split-brain-sentinel
description: Previent les conflits insolubles lors des experimentations paralleles dans différents corridors. Detecte la divergence entre branches soeurs et alerte en cas de modification conjointe du même module ou fichier de contrat.
version: 1.0.0
intent_hash: 0xAGENT_SPLIT_BRAIN_SENTINEL_20261025
---

# Agent Split-Brain Sentinel

## Objectif
Prevenir les conflits insolubles lors des experimentations paralleles dans différents corridors (ex: corridors 2, 3 et 4). Detecte la divergence entre branches soeurs derivees d'un meme commit main et alerte des que deux agents modifient le même module ou le même fichier de contrat.

## Declencheur
- Des que deux sessions travaillent simultanément sur deux worktrees distincts
- Avant chaque merge de branche feature
- Periodiquement (toutes les 30 minutes) pendant une session parallele

## Prerequis
- Repo git valide avec au moins deux branches actives derivees de main
- Accès en lecture aux diffs git entre branches
- Repertoire .kilo/ pour stocker les alertes

## Protocole

### Etape 1 - Identifier les branches actives derivees de main
```powershell
$defaultBranch = git symbolic-ref refs/remotes/origin/HEAD | ForEach-Object { $_.Split('/') | Select-Object -Last 1 }
$featureBranches = git branch --no-merged origin/$defaultBranch | ForEach-Object { $_.Trim() -replace '^\*', '' -replace '\s+', '' }
```

### Etape 2 - Calculer le hash de surface des signatures d'APIs et schémas ontologiques
Pour chaque branche active :
1. Extraire la liste des fichiers modifiés par rapport à main : `git diff main..<branch> --name-only`
2. Filtrer les fichiers de contrat (schemas, ontologies, APIs) : `*.json`, `*.yaml`, `*.ontology`, `*.api`
3. Calculer un hash de surface (SHA-256) du contenu concaténé de ces fichiers

### Etape 3 - Détecter les collisions
Comparer les ensembles de fichiers modifiés entre chaque paire de branches actives :
- Si deux branches modifient le même fichier de contrat -> alerte EARLY_COLLISION_WARNING
- Si deux branches modifient le même module métier -> alerte EARLY_COLLISION_WARNING

### Etape 4 - Lever l'alerte
Creer un fichier d'alerte dans .kilo/split_brain_alerts/ avec :
- `alert_type`: EARLY_COLLISION_WARNING
- `branches_involved`: liste des branches en collision
- `conflicting_files`: liste des fichiers en conflit
- `timestamp_utc`: horodatage ISO-8601
- `severity`: HIGH (fichier de contrat) ou MEDIUM (module métier)

## Sortie standard

```yaml
branches_active: <N>
branches_analyzed: <N>
collisions_detected: <C>
alerts_generated: <A>
errors: []
```

## Anti-patterns bloquants
- Ignorer une alerte EARLY_COLLISION_WARNING avant le merge
- Merger deux branches en collision sans résolution manuelle
- Ne pas surveiller les fichiers de contrat (schemas, ontologies)
- Ne pas exécuter le sentinel periodiquement pendant une session parallele

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xAGENT_SPLIT_BRAIN_SENTINEL_20261025
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed

## Script cible
`scripts/check_divergence.ps1`