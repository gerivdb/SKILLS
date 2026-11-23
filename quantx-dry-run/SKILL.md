---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_QUANTX_DRY_RUN_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : QuantX Dry-Run

## Déclencheur
Toute requête QUANTX nécessitant une simulation à sec avant exécution réelle. Principe fondamental : Intelligence = Pruning Dry-Run.

## Protocole

### Étape 1 — Simulation sans side-effects
Exécuter la logique cible sans modifier l'état du système (pas d'écriture disque, pas d'envoi réseau, pas de modification base de données).

### Étape 2 — Évaluation de pertinence
Pour chaque branche candidate, évaluer si elle apporte une valeur ajoutée par rapport à l'état actuel.

### Étape 3 — Élagage
Supprimer les branches non pertinentes. Conserver uniquement le sous-ensemble validé.

### Étape 4 — Décision go/no-go
Si le sous-ensemble validé est non vide et cohérent → go. Sinon → no-go.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de la décision dans le frontmatter.

## Dépendances
- `ontology-term-gate-extended` (S-13) pour valider le terme `pruning-dry-run`
- `registry-sync-extended` (S-14) pour vérifier les registres

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xQUANTX_DRY_RUN_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
