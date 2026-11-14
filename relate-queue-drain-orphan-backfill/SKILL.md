---
name: relate-queue-drain-orphan-backfill
description: Drain idempotent de la queue Relate/ENV3 et backfill des orphelins, avec heartbeats et preuves d'exécution sans doublons.
---
# relate-queue-drain-orphan-backfill

## Rôle
Assurer le **drain** des files de tâches/événements et le **backfill** des orphelins de manière **idempotente**, en maintenant la fraîcheur des heartbeats.

## Principes
- **Idempotence** : un item déjà traité (clé/id/session) ne doit pas être retraité ni dupliqué (ledger/DB).
- **Backfill orphelins** : détecter les entrées sans terminalisation et les rattacher/compléter selon le contrat de queue.
- **Append-only** : journalisation/ledger en ajout uniquement.

## Opérations
- Démons/scripts : `a_queue_drain_daemon.py` (cycles), composants Relate/backfill associés.
- Heartbeat : `shard_a` (et dépendants) dans `e2e_output/.heartbeat/`.
- Evidence : `queue_drain_evidence.json` / sorties de cycle (drained/total/err).

## Critères de succès
- `drained` cohérent, `err=None` (ou erreurs classées et retryables), pas de régression HWM/ledger.
- Heartbeats FRESH dans les TTL.

## Garde-fous
- Pas de purge destructive de queue/DB sans HITL ; pas d’appel LLM pour tâches déterministes.
