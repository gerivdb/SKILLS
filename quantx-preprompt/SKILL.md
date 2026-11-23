---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_QUANTX_PREPROMPT_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : QuantX Preprompt

## Déclencheur
Avant chaque requête QUANTX, injecter le pré-prompt contexte v3 pour activer le mode équipe horizontale sans le rappeler.

## Protocole

### Étape 1 — Charger le pré-prompt
Lire `PRE-PROMPT-QUANTX-V3.md` et injecter son contenu comme contexte d'activation.

### Étape 2 — Activer le mode équipe
Activer les 9 personae actives (C-P01 à C-P10, sans Gardener SUPERSEDED).

### Étape 3 — Activer les sections
Activer les 11 sections spécialisées : #archi, #grad, #perf, #ml, #usecase, #code, #sdk, #neuro, #assert, #merge, #mdu.

### Étape 4 — Activer les règles de collaboration
Édition parallèle asynchrone, gardien tournant, délibération flash 30s, arbitrage Bellard, fusion conditionnelle dans #merge.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de l'activation du pré-prompt.

## Dépendances
- `quantx-horizontal-engine` (S-01)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xQUANTX_PREPROMPT_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
