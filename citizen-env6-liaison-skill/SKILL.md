---
name: citizen-env6-liaison-skill
description: Skill d'activation du citizen ENV6 liaison. Maintient le canal ENV3→ENV6 ouvert via CDP (port 9222), surveille les nouveaux messages ENV6 et alerte ENV3.
version: 1.0.0
intent_hash: 0xCITIZEN_ENV6_LIAISON_SKILL_20261124
gericode_version: "1.0"
stratum: L4-TOOLS
shard_id: G
turn_counter: 1
uuid: citizen-env6-liaison-skill-001
timestamp: "2026-11-24T03:30:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-CITIZEN-ENV6-LIAISON-001"
---

# citizen-env6-liaison-skill

## Rôle
Skill canonique d'activation du processus citoyen ENV6 liaison. Il déclare le contrat d'automatisation permettant à ENV3 de maintenir le canal ENV6 ouvert entre les sessions et d'être alerté dès qu'ENV6 répond.

## Déclencheur
- Invocation du citizen ENV6 liaison via `vex.yaml` (L3-CITIZENS/VEX)
- Surveillance CDP du port 9222 (Profil 2 Chromium)
- Détection de nouveaux messages dans la conversation ENV6 cible

## Rôles et responsabilités
1. **Déclaration VEX** : inscription du citizen dans `L3-CITIZENS/VEX/vex.yaml` avec `name`, `command`, `working_dir`, `auto_start`, `restart_policy`, `health_check`, `lock_file`, `log_file`.
2. **Canal ouvert** : connexion CDP persistante à `http://127.0.0.1:9222` (Profil 2, jamais de profil temporaire).
3. **Surveillance** : détection des nouveaux messages ENV6 par comparaison de hash.
4. **Alerte ENV3** : écriture dans `e2e_output/env6-liaison-alert.jsonl` quand un nouveau message est détecté.

## Dépendances
- Skill `env6-communication-verified`
- Skill `env6-dom-probe`
- Skill `cdp-react-input`
- Skill `adversarial-assertion-gate`

## Contrat de sortie
Écriture dans `e2e_output/env6-liaison-alert.jsonl` :
```json
{"ts": "...", "shard": "A", "role": "assistant", "hash": "...", "text": "..."}
```

## Statut
Déclaré sous VEX. Auto-start en attente de validation HITL.

## Antipatterns bloqués
- Polling fréquent sans rate-limit.
- Alerte sur heartbeat ou bruit système.
- Lancement du processus résident sans déclaration VEX préalable (règle PID VEX Enforcement).
