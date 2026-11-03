---
name: process-hygiene
description: Detecte et purge les processus zombies et worktrees orphelins apres sessions KiloCode. Utilise ce skill quand tu dois nettoyer les processus legers residuels (git, node, python, zig, cargo, bun, pwsh, trixd, kix), les worktrees temporaires non fermes, ou les stashes anciens. Transverse a GeriCode, KIX, TRIX, KIVA-CLI.
version: 1.0.0
intent_hash: 0xPROCESS_HYGIENE_20260809
---

# Process Hygiene

## Objectif
Maintenir la proprete de l'environnement ENV2 (24 Go DDR3 ECC) en detectant et purgeant les processus zombies, worktrees orphelins et staches temporaires laisses par les sessions KiloCode, KIVA-CLI, TRIX et KIX.

## Declencheur
- Fin de session KiloCode
- Avant tout lancement Agent Manager
- Apres crash ou interruption d'un processus
- Audit quotidien
- Avant compilation TRIX ou session d'isolation

## Prerequis
- Acces en ecriture au systeme (Stop-Process, git worktree)
- Acces en lecture aux processus systeme
- Remote `origin` configure pour les operations git

## Criteres de detection - Processus zombies

Un processus est considere comme zombie si TOUTES les conditions suivantes sont reunies :

| Critere | Valeur |
|---------|--------|
| `MainWindowTitle` | Vide |
| `CPU` | Proche de 0 (< 0.5s cumule) |
| `WorkingSet` | < 10 Mo |
| `StartTime` | > 1h |

### Types de processus surveilles

| Type | Pattern | Impact |
|------|---------|--------|
| `git.exe` | clones, pulls, merges | handles Windows, RAM |
| `node.exe` | Agent Manager | RAM, threads |
| `python.exe` | KIX, scripts | RAM, handles |
| `zig.exe` | compilation TRIX | CPU, RAM temporaire |
| `cargo.exe` | builds Rust | CPU, RAM temporaire |
| `bun.exe` | scripts JS | RAM |
| `pwsh.exe` | shells PowerShell | handles |
| `trixd.exe` | runtime TRIX | handles, namespaces |
| `kix.exe` | orchestrateur KIX | RAM, ports |

## Protocole

### Etape 1 - Detection des processus zombies

```powershell
# PowerShell - lister les processus cibles
$targets = @("git", "node", "python", "zig", "cargo", "bun", "pwsh", "trixd", "kix")
$now = Get-Date
$zombies = @()

foreach ($name in $targets) {
    $procs = Get-CimInstance Win32_Process -Filter "Name LIKE '%$name%'" -ErrorAction SilentlyContinue
    foreach ($p in $procs) {
        try {
            $proc = Get-Process -Id $p.ProcessId -ErrorAction Stop
            $ageHours = if ($proc.StartTime) { ($now - $proc.StartTime).TotalHours } else { 0 }
            $memMB = [math]::Round($proc.WorkingSet64 / 1MB)
            if ($proc.MainWindowTitle -eq "" -and $proc.CPU -lt 0.5 -and $memMB -lt 10 -and $ageHours -gt 1) {
                $zombies += $proc
            }
        } catch { }
    }
}
```

### Etape 2 - Detection des worktrees orphelins

```powershell
# Lister les worktrees
git worktree list

# Verifier que chaque worktree pointe vers une branche existante
$wtList = git worktree list --porcelain
# Parser et identifier les worktrees dont la branche n'existe plus
```

### Etape 3 - Detection des stashes temporaires

```powershell
# Lister les stashes
git stash list

# Identifier les stashes temporaires (temp, WIP, before switch)
# Supprimer les stashes > 7 jours
```

### Etape 4 - Purge orchestree

| Type | Commande de purge | Risque |
|------|-------------------|--------|
| `git.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `node.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `python.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `zig.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `cargo.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `bun.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `pwsh.exe` zombie | `Stop-Process -Id <pid> -Force` | Faible |
| `trixd.exe` zombie | `Stop-Process -Id <pid> -Force` | Moyen (isolation) |
| `kix.exe` zombie | `Stop-Process -Id <pid> -Force` | Moyen (orchestrateur) |
| Worktree orphelin | `git worktree remove <path>` | Faible |
| Worktree orphelin (branch supprimee) | `git worktree prune` | Faible |
| Stash temporaire | `git stash drop stash@{n}` | Faible |

### Etape 5 - Logging NEXUS/WAL

Toute purge doit etre loggee dans NEXUS/WAL :

```json
{
  "timestamp": "2026-08-09T20:00:00Z",
  "event_type": "process_zombie_purge",
  "intent_hash": "0xPRD_MOC_PROCESS_ZOMBIE_HYGIENE_DEVTOOLS_20260809",
  "data": {
    "purged": [
      {"type": "git", "pid": 1234, "name": "git.exe"}
    ],
    "wal_logged": true
  }
}
```

## Regles de purge

1. **Dry-run par defaut** - toujours proposer l'inventaire avant purge
2. **Purge par type** - demander confirmation par type de processus
3. **Ne JAMAIS purger** :
   - Processus avec MainWindowTitle non vide (application active)
   - Processus dont le PID < 100 (systeme Windows)
   - `trixd.exe` sans verification prealable (isolation en cours)
   - `kix.exe` sans verification prealable (orchestrateur actif)
4. **Worktrees** - verifier que la branche existe avant suppression
5. **Stashes** - ne jamais purger sans inspection du contenu

## Sortie standard

```yaml
process_zombies: []
worktree_zombies: []
stash_zombies: []
purged: []
wal_logged: true
recommendations: []
```

## Integration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1` (CHECK-8)
- **KIX** : `src/zombie_monitor.py` (endpoints `/health/zombies`, `/health/zombies/purge`)
- **TRIX** : `tools/trix_preflight.zig` (child zombie check)
- **KIVA-CLI** : `docs/KIVACLI-GIT-ZOMBIE-HOOKS.md` (pre/post CI hooks)

## Reference ADR

- **ADR** : ADR-2026-08-09-001-GIT_HYGIENE_MECHANISMS
- **IntentHash** : `0xGIT_HYGIENE_RULES_20260809`
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed
- **Maj requise si** : statut ADR passe a deprecated ou superseded

## References

- **IntentHash parent** : `0xPRD_MOC_PROCESS_ZOMBIE_HYGIENE_DEVTOOLS_20260809`
- **PRD source** : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-PROCESS-ZOMBIE-HYGIENE-DEVTOOLS-2026-08-09.md`
