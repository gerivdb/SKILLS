# Skill: skill-wal-auditor

## Description
Audite chaque fichier WAL : cohérence nom/timestamp, sémantique scellée (P6),
présence des champs obligatoires (friction, entropy, return_code, merkle_leaf),
et présence du champ `pid_role` (server / test_process / wrapper).

## Déclencheurs
- "auditer WAL", "vérifier WAL", "wal-auditor"

## Règles
- Le fichier WAL doit avoir un nom au format `0x244-*` ou `0x243-*`
- Le `timestamp_utc` doit correspondre au timestamp dans le nom de fichier (±5 min)
- Les champs `friction`, `entropy`, `return_code`, `merkle_leaf` doivent être présents
- Le champ `pid_role` doit être présent (`server`, `test_process`, ou `wrapper`)

## Invariants
- Aucun WAL ne peut avoir `return_code: 0` avec `friction: 1.0` ou `entropy: 1.0`
- Aucun WAL ne peut avoir `transport: cdp` avec `injected: false` sans justification explicite

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["auditer WAL", "vérifier WAL", "wal-auditor"]
- domaine: gouvernance
- phi_weight: 0.005
- assimilation_status: N/A