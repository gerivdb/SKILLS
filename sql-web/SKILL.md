---
name: sql-web
description: Explorateur web local binaire unique en Rust — interface web locale légère pour parcourir les tables SQLite avec pagination et mode lecture seule. Pattern inspiré de https://github.com/YinMo19/sql-web
version: 1.0.0
intent_hash: 0xSKILL_SQL_WEB_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/YinMo19/sql-web
source_url: https://github.com/YinMo19/sql-web
path: sql-web
---

# sql-web — Skill KiloCode

## Objectif

Fournir un explorateur web local léger (binaire unique en Rust) pour parcourir les tables SQLite avec pagination et mode lecture seule. Adapté à ENV2 pour l'accès web local aux bases SQLite sans serveur externe.

## Déclencheur

Ce skill s'active quand :
- Il faut parcourir des tables SQLite via une interface web locale légère
- La pagination des résultats est nécessaire pour de gros volumes
- Un mode lecture seule est requis pour préserver l'intégrité des données
- Un binaire unique Rust est préféré pour la simplicité de déploiement sur ENV2

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `port` | integer | ❌ | Port local pour l'interface web (défaut: 8080) |
| `read_only` | boolean | ❌ | Forcer le mode lecture seule (défaut: true) |
| `page_size` | integer | ❌ | Nombre de lignes par page (défaut: 50) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `server_url` | string | URL de l'interface web locale |
| `tables_browsed` | array | Tables parcourues via l'interface web |
| `page_count` | integer | Nombre de pages naviguées |
| `read_only_mode` | boolean | True si le mode lecture seule était actif |
| `evidence_hash` | string | Hash SHA-256 de la session web |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Lancement de l'explorateur web

```
→ Lancer sql-web sur la base cible avec le port spécifié
→ Activer le mode lecture seule
→ Parcourir les tables avec pagination
```

### Étape 3 — Preuve d'exécution

```
→ Capturer l'URL du serveur et les tables parcourues
→ Calculer le hash SHA-256 de la session
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un serveur web externe ou cloud pour l'exploration SQLite
- ❌ Désactiver le mode lecture seule sans autorisation explicite
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
