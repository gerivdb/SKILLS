---
name: reglite
description: Extension opérateur regex léger — correspondance d'expressions régulières sur colonnes texte et blob dans SQLite. Pattern inspiré de https://github.com/caido/reglite
version: 1.0.0
intent_hash: 0xSKILL_REGLITE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/caido/reglite
source_url: https://github.com/caido/reglite
path: reglite
---

# reglite — Skill KiloCode

## Objectif

Fournir une extension opérateur regex léger pour SQLite permettant la correspondance d'expressions régulières sur colonnes texte et blob. Adapté à ENV2 pour la recherche regex légère sans dépendances lourdes.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer une correspondance regex légère sur des colonnes texte ou blob SQLite
- Une extension regex minimale est préférée à des outils externes lourds
- La recherche doit rester dans l'environnement SQL pour la cohérence
- L'environnement ENV2 nécessite une empreinte mémoire réduite

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `table_name` | string | ✅ | Nom de la table à rechercher |
| `column_name` | string | ✅ | Nom de la colonne texte ou blob à filtrer |
| `regex_pattern` | string | ✅ | Motif d'expression régulière |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `matching_rows` | array | Lignes correspondant au motif regex |
| `match_count` | integer | Nombre de lignes correspondantes |
| `extension_loaded` | string | Nom de l'extension chargée (reglite) |
| `evidence_hash` | string | Hash SHA-256 des résultats |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
→ Vérifier que l'extension reglite est chargée dans la session
```

### Étape 2 — Recherche regex

```
→ Exécuter une requête SQL utilisant l'opérateur reglite sur la colonne cible
→ Retourner les lignes correspondantes
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 des résultats
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep` sur des fichiers bruts au lieu d'une recherche regex SQL structurée
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant la recherche regex en lecture
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
