---
name: cache-cleaner
description: Nettoie et purifie les caches de build et d'exécution (__pycache__, .pytest_cache, .ruff_cache, .benchmarks, .swarm, node_modules/.cache, etc.) dans L4-TOOLS, L3-CITIZENS et les worktrees associés. Utilise ce skill quand tu dois libérer de l'espace disque, supprimer des caches obsolètes, ou préparer un environnement propre avant compilation.
version: 1.0.0
intent_hash: 0xSKILL_CACHE_CLEANER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/cache-cleaner/SKILL.md
---

# Skill — cache-cleaner

## Objectif

Maintenir la propreté des répertoires de build et d'exécution en détectant et supprimant les caches obsolètes, temporaires ou orphelins générés par Python, Rust, Node/Bun, Zig, Cargo et les outils d'analyse du repo.

## Déclencheur

- Avant toute compilation ou build (TRIX, KIX, Agent Manager)
- Audit hebdomadaire de l'espace disque
- Après changement de branche ou de worktree
- Quand `node_modules`, `__pycache__` ou `.pytest_cache` deviennent volumineux
- Avant archivage ou transfert de worktree

## Prérequis

- Accès en écriture aux répertoires cibles
- PowerShell 5.1+ ou Bash
- Connaissance des répertoires à protéger (ne jamais supprimer `node_modules` actif sans confirmation)

## Répertoires de cache cibles

| Type | Pattern | Emplacement typique | Risque |
|------|---------|---------------------|--------|
| Python | `__pycache__` | Partout dans `src/`, `tests/`, `.kilo/` | Faible |
| Python | `.pytest_cache` | Racine du repo | Faible |
| Python | `.ruff_cache` | Racine du repo | Faible |
| Python | `.mypy_cache` | Racine du repo | Faible |
| JS/TS | `node_modules/.cache` | `kilocode/`, `act-protocol/` | Moyen |
| Bun | `.bun` | Racine du repo | Faible |
| Build | `.benchmarks` | Racine du repo | Faible |
| Build | `.swarm` | Racine du repo | Faible |
| Build | `.kilo/.pytest_cache` | `.kilo/` | Faible |
| Zig | `zig-cache/` | `src/zig/`, `TRIX/` | Moyen |
| Cargo | `target/` | `TRIX/`, `KIX/` | Élevé (gros) |

## Protocole

### Étape 1 — Inventaire des caches

```powershell
# Lister les caches détectés avec leur taille
Get-ChildItem -Path <repo> -Recurse -Include __pycache__, .pytest_cache, .ruff_cache, .bun, .benchmarks, .swarm -Directory | 
  Select-Object FullName, @{N='SizeMB';E={[math]::Round((Get-ChildItem $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB, 2)}}
```

### Étape 2 — Vérification de protection

Avant suppression, vérifier que le cache n'est pas verrouillé par un processus actif :
- `git fsmonitor--daemon` en cours → ne pas toucher `node_modules/.cache`
- Compilation Zig/Cargo en cours → ne pas toucher `zig-cache/` ou `target/`
- Session Agent Manager active → ne pas toucher `.kilo/` caches

### Étape 3 — Purge orchestrée

```powershell
# Exemple : suppression d'un __pycache__
Remove-Item -Path "<chemin>\__pycache__" -Recurse -Force

# Exemple : suppression de .pytest_cache
Remove-Item -Path "<repo>\.pytest_cache" -Recurse -Force
```

### Étape 4 — Logging NEXUS/WAL

Toute purge doit être loggée :

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "cache_cleaner_purge",
  "intent_hash": "0xSKILL_CACHE_CLEANER_20261105",
  "data": {
    "caches_purged": [
      {"type": "__pycache__", "path": "src/act/__pycache__", "size_mb": 12.5}
    ],
    "total_size_freed_mb": 45.2,
    "wal_logged": true
  }
}
```

## Règles de nettoyage

1. **Dry-run par défaut** : toujours lister avant suppression
2. **Jamais supprimer** un cache verrouillé par un processus actif
3. **Jamais supprimer** `node_modules` complet sans confirmation HITL
4. **Seuil de taille** : signaler si un cache dépasse 500 Mo
5. **Conserver** les caches de build actifs (< 24h d'utilisation)

## Sortie standard

```yaml
caches_scanned: 24
caches_purged: []
caches_kept: []
total_size_freed_mb: 0
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Supprimer `__pycache__` pendant une exécution Python active
- Supprimer `target/` (Cargo) pendant une compilation Rust
- Utiliser `Remove-Item -Recurse -Force` sans'inventaire préalable
- Négliger le logging WAL après purge

## Intégration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1`
- **KIX** : `src/zombie_monitor.py`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-CACHE_HYGIENE_MECHANISMS
- **IntentHash** : 0xSKILL_CACHE_CLEANER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed