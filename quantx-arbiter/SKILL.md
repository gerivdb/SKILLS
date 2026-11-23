---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_QUANTX_ARBITER_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : QuantX Arbiter

## Déclencheur
Conflit entre sections spécialisées lors de l'édition parallèle asynchrone. Nécessite un arbitrage pour trancher.

## Protocole

### Étape 1 — Délibération flash
Ouvrir une délibération de 30 secondes maximum entre les personas en conflit.

### Étape 2 — Arbitrage Bellard
Si aucun consensus à l'expiration des 30s, Bellard (C-P07) tranche définitivement.

### Étape 3 — Fusion conditionnelle
Si assertions OK (`#assert` validé) et entropie basse → fusion automatique dans `#merge`.

### Étape 4 — Horodatage UTC
Enregistrer l'horodatage UTC de la décision d'arbitrage.

## Dépendances
- `quantx-horizontal-engine` (S-01)
- `ontology-term-gate-extended` (S-13) pour valider `arbitrage-mecanism`

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xQUANTX_ARBITER_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
