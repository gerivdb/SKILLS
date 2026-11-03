---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_APF_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/agent-process-forensics/SKILL.md
---

# Skill - agent-process-forensics

## Objectif

Cartographier l'arbre des processus Windows (Parent-PID), detecter les daemons orphelins (`kilo.exe`, `node.exe`, `pwsh.exe`) et eliminer les instances zombies issues de reloads d'agents non termines. Couche OS & Arborescence.

## Declencheur

- Zone de saisie agent absente / interface blanche / reflexion infinie.
- Reload VS Code laissant des processus `kilo.exe` ou `node.exe` residuels.
- Avant toute reinitialisation d'etat agent (pre-remediation).

## Entrees

Aucune (scan systematique de l'OS).

## Sorties

- Rapport JSON d'arbre des processus suspects.
- Liste des PIDs zombies elimines.
- Entree WAL NEXUS horodatee.

## Regles

### 1. Scanner l'arbre des processus (CIM/WMI)

Utiliser `Win32_Process` via CIM pour recuperer :
- ProcessId, ParentProcessId, Name, CommandLine, CreationDate.

### 2. Filtrer par ligne de commande

Cibles prioritaires :
- `kilo.exe` - processus agent Kilo Code residuel.
- `node.exe` - runtime Node lie aux webviews agents.
- `pwsh.exe` / `powershell.exe` - shells orphelins de reloads.

### 3. Detecter les zombies

Un processus est considere zombie s'il remplit une des conditions :
- Parent PID = 1 (orphelin reparente) ET age > 30 min.
- Nom `kilo.exe` ET aucune fenetre principale visible.
- Nom `node.exe` ET ligne de commande contenant `kilo` ou `vscode-webview`.

### 4. ?liminer les instances

- Tenter `CloseMainWindow()` d'abord (arret gracieux).
- Si echec apres 10 s -> `Kill()` force.
- Journaliser chaque PID elimine avec motif.

## Script d'investigation

`scripts/investigate.ps1` - voir ci-dessous.

## Tests

- `tests/test_agent_process_forensics.ps1` - scanner sans elevation, verifier sortie JSON valide.

## Probes

- Aucun processus `kilo.exe` zombie persistant > 10 min apres reload agent.
- Zero processus orphelin Parent PID = 1 avec age > 30 min.

## WAL NEXUS

```
[WAL_NEXUS] skill=agent-process-forensics action=scan timestamp=<ISO> zombies_detected=<n> pids_eliminated=<list>
[WAL_NEXUS] skill=agent-process-forensics action=eliminate timestamp=<ISO> pid=<PID> name=<Name> reason=<motif> status=<OK|FAIL>
```

## Reference ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
