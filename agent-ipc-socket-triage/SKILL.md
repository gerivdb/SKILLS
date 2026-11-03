---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_IST_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/agent-ipc-socket-triage/SKILL.md
---

# Skill - agent-ipc-socket-triage

## Objectif

Refuter les faux conflits de ports et auditer les connexions TCP locales (ports 4096, 61020, etc.). Identifier les sockets en etat *Half-Open* ou *CLOSE_WAIT* bloquant les generateurs asynchrones de streaming (Reasoning / Thinking). Couche Reseau & Flux SSE.

## Declencheur

- Conflit de port presume au demarrage d'un agent.
- Streaming SSE interrompu / chunks manquants.
- Generateur asynchronique bloque (Reasoning / Thinking fige).
- Port 4096 ou 61020 deja utilise selon un message d'erreur.

## Entrees

- `target_port`: port TCP a auditer (defaut : 4096, 61020).

## Sorties

- Rapport JSON des connexions TCP locales par etat.
- Liste des sockets Half-Open / CLOSE_WAIT bloquantes.
- Entree WAL NEXUS horodatee.

## Regles

### 1. Auditer les connexions TCP locales

Utiliser `Get-NetTCPConnection` pour lister :
- LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess.

### 2. Filtrer par ports cibles

Ports prioritaires :
- 4096 - flux SSE / streaming agent.
- 61020 - communication interne Kilo Code / Cline.

### 3. Detecter les etats bloquants

Etats consideres comme bloquants :
- `CLOSE_WAIT` - fermeture distante non acquittee (socket zombie).
- `Half-Open` - etat intermediaire sans trafic inter-chunks.
- `TIME_WAIT` prolonge > 60 s - epuisement de la plage ephemere.

### 4. Detecter l'absence de trafic inter-chunks

- Surveiller un socket etabli sans echange de donnees > 30 s pendant un streaming actif.
- Considere comme un blocage de generateur asynchronique.

### 5. Refutation des faux conflits

- Un port en `LISTEN` avec un processus legitime n'est pas un conflit.
- Un port en `TIME_WAIT` sans `CLOSE_WAIT` associe est normal (pas d'action).

## Script d'investigation

`scripts/triage.ps1` - voir ci-dessous.

## Tests

- `tests/test_agent_ipc_socket_triage.ps1` - auditer le port 4096, verifier que la sortie JSON est valide.

## Probes

- Zero socket `CLOSE_WAIT` persistant > 60 s sur les ports 4096 / 61020.
- Zero socket `Half-Open` sans trafic > 30 s pendant streaming SSE.

## WAL NEXUS

```
[WAL_NEXUS] skill=agent-ipc-socket-triage action=audit timestamp=<ISO> port=<PORT> connections=<n> blocking=<m>
[WAL_NEXUS] skill=agent-ipc-socket-triage action=refute_false_conflict timestamp=<ISO> port=<PORT> reason=<motif>
```

## Reference ADR

- **ADR** : ADR-2026-08-24-001-WIN32-SINGLETON-BIND
- **IntentHash** : 0xWIN32_SINGLETON_BIND_20260824
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : draft (PRD GEN-012)
