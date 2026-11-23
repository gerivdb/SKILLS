---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_ONTOLOGY_TERM_GATE_EXTENDED_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Ontology Term Gate Extended

## Déclencheur
Validation active des termes ontologiques avant écriture de documents gouvernants (PRD, ADR, INTENT, EPIC, README). Bloque l'usage de termes non déclarés dans ONTOLOGY/ONTOLOGY.yaml.

## Protocole

### Étape 1 — Lire le document cible
Extraire tous les termes techniques utilisés dans le document.

### Étape 2 — Vérifier contre ONTOLOGY.yaml
Pour chaque terme, vérifier qu'il existe comme `id` dans `ONTOLOGY/ONTOLOGY.yaml` ou comme fichier dans `ONTOLOGY/concepts/`.

### Étape 3 — Rapport
- `[OK]` terme trouvé et lié à son fichier concept
- `[cover]` terme couvert par un concept parent
- `[MISS]` terme absent → définir avant implémentation

### Étape 4 — Créer les concepts manquants
Pour chaque terme `[MISS]`, créer un fichier `ONTOLOGY/concepts/<slug>.md` avec définition N/N+1/N+2.

## Termes déjà validés
- `collaborative-horizontal-protocol` → collaborative-horizontal-protocol.md
- `horodatage-utc` → horodatage-utc.md
- `inherits` → inherits.md
- `keep-entities` → keep-x---help.md (cover)
- `keep-x` → keep-x.md
- `keep-x---help` → keep-x---help.md
- `ontology-declaration` → ontology-declaration.md
- `ontology-declaration-quantx` → ontology-declaration-quantx.md
- `parameters` → open-weights-apache2.md (cover)
- `pruning-dry-run` → pruning-dry-run.md
- `quantx` → quantx.md
- `quantx---help` → quantx---help.md
- `sidekeep-x` → sidekeep-x.md

## Dépendances
- `ONTOLOGY/ONTOLOGY.yaml` (source de vérité)
- `ONTOLOGY/concepts/` (dossier des concepts)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xSKILL_ONTOLOGY_TERM_GATE_EXTENDED_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
