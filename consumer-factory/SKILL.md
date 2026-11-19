---
type: skill
version: 1.0.0
gericode_version: 2.0
stratum: L4-TOOLS
shard_id: dispatcher
turn_counter: 1
uuid: 8f4e2a1c-9b3d-4e5f-a6c7-1d2e3f4a5b6c
timestamp: 2026-11-19T12:00:00Z
invariants: [ZCF-0.0, atomicité, déterminisme, idempotence]
wal_reference: 0x243
status: active
date: 2026-11-19
intent_hash: 0xCONSUMER_FACTORY_SKILL_20261119
---
# Skill : consumer-factory

## Rôle
Générer de manière déterministe un script consumer paramétrique capable d'exécuter une mission spécifique tout en respectant strictement le contrat FSM de `mission_fsm_engine`.

## Entrées (I)
- `mission_id` : Identifiant unique de la mission.
- `shard_id` : Identifiant du shard cible (ex: A, F, C).
- `execution_hook` : Chemin ou définition de la fonction métier à exécuter.
- `timeout_seconds` : Délai maximal d'exécution avant basculement en `blocked`.

## Sorties (O)
- Fichier Python exécutable (`consumer_<shard_id>.py`) incluant :
  1. Import et initialisation de `mission_fsm_engine`.
  2. Appel à `claim(mission_id)` (verrouillage exclusif avec lease).
  3. Exécution du `execution_hook` avec gestion d'exception stricte.
  4. Appel à `complete(mission_id, ack_token)` en cas de succès, ou `block(mission_id, reason)` en cas d'échec/timeout.
  5. Nettoyage et libération des ressources.

## Invariants M3
- **Zéro dépendance externe** : stdlib Python uniquement.
- **Idempotence** : l'exécution multiple du même consumer sur la même mission ne doit pas corrompre l'état FSM (géré par le lock exclusif de l'engine).
- **Preuve brute** : chaque transition FSM doit être journalisée dans le WAL de l'engine.
- **Fail-Fast** : toute anomalie de parsing ou d'environnement déclenche un `block` immédiat, jamais un état `in_progress` fantôme.
