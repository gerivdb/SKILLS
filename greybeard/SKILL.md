---
name: greybeard
description: Skills de contrôle et de vérification d'exécution pour agents. Pattern inspiré de https://github.com/clawnify/greybeard
version: 1.0.0
intent_hash: 0xSKILL_GREYBEARD_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/clawnify/greybeard
source_url: https://github.com/clawnify/greybeard
path: greybeard
---

# Greybeard — Skill KiloCode

## Objectif

Fournir des skills de contrôle et de vérification d'exécution pour agents. Ce skill encapsule le pattern du repo externe `greybeard` adapté à ENV2, avec respect des règles de preuve fraîche, de non-paraphrase et de traçabilité WAL.

## Déclencheur

Ce skill s'active quand :
- Une exécution d'agent doit être contrôlée et vérifiée
- Un résultat d'outil doit être vérifié contre une preuve brute
- Une déclaration de succès doit être auditée pour absence de paraphrase
- Une traçabilité WAL doit être imposée sur une action

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `action_trace` | string | ✅ | Trace d'action à vérifier |
| `expected_proof` | object | ❌ | Preuve attendue (hash, timestamp, code de retour) |
| `verification_type` | enum | ✅ | stdout / hash / git_status / dom / wal |
| `target_entity` | string | ❌ | Entité cible (fichier, repo, skill, processus) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `verification_result` | enum | passed / failed / inconclusive |
| `actual_proof` | object | Preuve réelle trouvée (hash, timestamp, code de retour) |
| `mismatch_details` | string | Détails de non-concordance si applicable |
| `wal_entry` | string | Référence d'entrée WAL créée |
| `evidence_hash` | string | Hash SHA-256 du résultat de vérification |

## Protocole Obligatoire

### Étape 1 — Capture de la trace d'action

```
→ Lire la trace d'action à vérifier (stdout, logs, git diff, fichiers modifiés)
→ Identifier l'entité cible (fichier, repo, skill, processus)
→ Déterminer le type de vérification nécessaire
```

### Étape 2 — Vérification par preuve brute

```
→ Si verification_type = stdout → capturer la sortie brute de la commande
→ Si verification_type = hash → recalculer le hash SHA-256 sur le fichier actuel
→ Si verification_type = git_status → vérifier que git status est propre
→ Si verification_type = dom → capturer le DOM actuel via CDP
→ Si verification_type = wal → vérifier l'entrée dans le WAL (WAL-0x243)
```

### Étape 3 — Comparaison avec la preuve attendue

```
→ Comparer la preuve réelle avec la preuve attendue (si fournie)
→ Vérifier que le hash SHA-256 correspond
→ Vérifier que l'horodatage UTC est frais (pas de recopiage d'ancien rapport)
→ Vérifier qu'il n'y a pas de paraphrase (règle verbatim-fidelity)
```

### Étape 4 — Enregistrement WAL

```
→ Créer une entrée WAL avec le résultat de vérification
→ Enregistrer le hash SHA-256 et l'horodatage UTC
→ Mettre à jour skills-index.json si le skill vérifié est modifié
→ Produire le hash SHA-256 du résultat de vérification
```

## Anti-patterns

- ❌ Vérifier une exécution sans preuve brute (stdout, hash, timestamp)
- ❌ Accepter une déclaration de succès sans preuve correspondante
- ❌ Utiliser un hash recopié d'un rapport précédent (règle proof-recalculation)
- ❌ Paraphraser le résultat au lieu de citer textuellement (règle verbatim-fidelity)

## Référence ADR

- **ADR** : ADR-2026-11-16-001-ZERO-TRUST-EVIDENCE
- **IntentHash** : (lié au ADR de zéro confiance sur les preuves)
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : proof-recalculation
- **Règle** : verbatim-fidelity
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
