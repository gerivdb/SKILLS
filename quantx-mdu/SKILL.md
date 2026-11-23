---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_QUANTX_MDU_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : QuantX MDU

## Déclencheur
Toute opération QUANTX nécessitant la cohérence de l'écosystème GERIVDB, le métacluster, les flux inter-dépôts, et la section #mdu.

## Protocole

### Étape 1 — Vérifier les registres
Vérifier `known_repositories.yaml`, `ECOS_ROOT.json`, et le registre TOPOS pour cohérence.

### Étape 2 — Surveiller les flux inter-dépôts
Détecter les flux atomiques (MULTI_GIT_SWARM_FLOW pattern) entre les dépôts.

### Étape 3 — Détecter la dérive
Identifier les atomes orphelins, les designs sans référence ontologique, et les dérives de registre.

### Étape 4 — Générer des alertes
En cas de dérive, générer une alerte vers le Gardien MDU (C-P10).

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de chaque vérification de cohérence.

## Dépendances
- `quantx-mdu` citizen (C-04 dans vex.yaml)
- `registry-sync-extended` (S-14)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xQUANTX_MDU_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
