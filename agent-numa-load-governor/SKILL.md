---
name: agent-numa-load-governor
description: Empêche le freeze physique de l'OS et de VS Code sur la machine de dev (dual Xeon E5620 NUMA) en throttlant les subagents selon la disponibilité RAM/CPU.
version: 1.0.0
intent_hash: 0xAGENT_NUMA_LOAD_GOVERNOR_20261025
---

# Agent NUMA Load Governor

## Objectif
Empêcher le freeze physique de l'OS et de VS Code sur la station de développement (dual Xeon E5620 NUMA, 24 Go DDR3 ECC). Le gouverneur mesure la RAM disponible et l'utilisation CPU, et suspend temporairement les subagents non prioritaires lorsque les seuils sont dépassés. Il assigne aussi l'affinité CPU par noeud NUMA pour isoler le serveur IDE des workers d'exécution.

## Declencheur
- Lancement d'une tâche lourde (build, tests pytest, inférence)
- Demarrage d'une session parallele
- Verification periodique (toutes les 5 minutes) pendant une session active

## Prerequis
- Windows avec PowerShell 7+
- Accès en lecture aux compteurs de performance système (Get-CimInstance, Get-Process)
- Accès en ecriture pour modifier l'affinité CPU des processus (Set-ProcessAffinity)

## Protocole

### Etape 1 - Mesurer la mémoire RAM disponible
```powershell
$mem = Get-CimInstance Win32_OperatingSystem
$freeMB = [math]::Round($mem.FreePhysicalMemory / 1024)
$totalMB = [math]::Round($mem.TotalVisibleMemorySize / 1024)
```

### Etape 2 - Mesurer le taux d'utilisation CPU
```powershell
$cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1
$cpuPercent = $cpu.CounterSamples.CookedValue
```

### Etape 3 - Appliquer le throttling
| Condition | Action |
|-----------|--------|
| RAM libre >= 3 Go ET CPU <= 85% | Aucun throttling, execution normale |
| RAM libre < 3 Go OU CPU > 85% | Suspendre les subagents non prioritaires (SIGSTOP ou file d'attente) |
| RAM libre < 1 Go OU CPU > 95% | Suspendre TOUS les subagents, alerte critique |

### Etape 4 - Assigner l'affinité CPU par noeud NUMA
- Noeud NUMA 0 : serveur IDE (VS Code, webview)
- Noeud NUMA 1 : workers d'exécution (subagents, builds, tests)
- Utiliser `Set-ProcessAffinity` ou le paramètre de démarrage pour isoler les processus

### Etape 5 - Reprise des subagents suspendus
Lorsque la RAM remonte au-dessus de 4 Go ET que le CPU redescend en dessous de 70%, reprendre les subagents suspendus dans l'ordre de priorité.

## Sortie standard

```yaml
ram_free_gb: <X.X>
ram_total_gb: <X.X>
cpu_percent: <Y.Y>
throttling_applied: true|false
subagents_suspended: <N>
numa_node_ide: 0
numa_node_workers: 1
errors: []
```

## Anti-patterns bloquants
- Ne jamais vérifier les ressources avant de lancer une session parallele
- Suspendre le processus IDE lui-même
- Ne pas reprendre les subagents quand les ressources redeviennent disponibles
- Ne pas isoler l'affinité CPU (IDE et workers sur le même noeud NUMA)

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xAGENT_NUMA_LOAD_GOVERNOR_20261025
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed

## Script cible
`scripts/throttle_agents.ps1`