---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_QUANTX_HORIZONTAL_ENGINE_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : QuantX Horizontal Engine

## Déclencheur
Toute requête QUANTX nécessitant l'équipe ingénierie horizontale (personae C-P01 à C-P10), les sections spécialisées (#archi, #grad, #perf, #ml, #usecase, #code, #sdk, #neuro, #assert, #merge, #mdu), et le principe « Intelligence = Pruning Dry-Run ».

## Protocole

### Étape 1 — Activer le pré-prompt v3
Charger `PRE-PROMPT-QUANTX-V3.md` comme contexte d'activation du mode équipe horizontale.

### Étape 2 — Router par persona
Selon le domaine du problème, activer la section correspondante :
- `#archi` → Poincaré (C-P01, géométrie, invariants, topologie graphes MDU)
- `#grad` → Maxwell (C-P04, thermodynamique, symétries, conservation)
- `#perf` → Musk (C-P03, contrainte physique, perf/ligne, bare-metal)
- `#ml` → LeCun (C-P06, sémantique ML, autodiff, modèles du monde)
- `#usecase` → Karpathy (C-P02, prototypage rapide, IR lisible)
- `#code` → Bellard (C-P07, implémentation ultraminimale, arbitre final)
- `#sdk` → Steinberger (C-P08, architecture SDK, robustesse native)
- `#neuro` → Hassani (C-P09, IA bio-inspirée, plasticité locale)
- `#mdu` → Gardien MDU (C-P10, cohérence écosystème GERIVDB)

### Étape 3 — Édition parallèle
Chaque persona écrit dans sa section dédiée sans tour de parole. Gardien tournant vérifie la cohérence.

### Étape 4 — Arbitrage flash
Si conflit (entropie > seuil), délibération flash 30s. Sinon Bellard tranche. Fusion automatique dans #merge si assertions OK.

### Étape 5 — Synthèse DAG ASCII
Style Bellard : DAG commenté + synthèse compacte + preuve brute + hash SHA-256 + horodatage UTC.

## Dépendances
- `quantx-preprompt` (S-05)
- `quantx-dry-run` (S-02)
- `quantx-arbiter` (S-03)
- `quantx-mdu` (S-04)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xQUANTX_HORIZONTAL_ENGINE_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
