---
name: sqlite-tui-pastalikek65
description: Visionneuse TUI SQLite binaire unique — affiche tables, lignes et taille WAL en terminal sans CGO (<40 Mo RAM). Pattern inspiré de https://github.com/Pastalikek65/sqlite-tui
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_TUI_PASTALIKEK65_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Pastalikek65/sqlite-tui
source_url: https://github.com/Pastalikek65/sqlite-tui
path: sqlite-tui-pastalikek65
---

# SQLite TUI (Pastalikek65) — Skill KiloCode

## Objectif

Fournir une visionneuse TUI SQLite binaire unique pour naviguer dans les bases SQLite locales d'ENV2 sans recharger à chaque accès. Affiche tables, lignes et taille WAL en terminal, avec une empreinte mémoire <40 Mo. Adapté à la station HP Z600 (legacy, 24 Go RAM, CPU limité).

## Déclencheur

Ce skill s'active quand :
- Il faut explorer une base SQLite locale sur ENV2 sans installer de client lourd
- Une navigation rapide dans les tables/WAL est nécessaire pour diagnostiquer une dérive
- L'accès doit rester en mode lecture seule pour préserver l'intégrité des données
- Un outil TUI léger est préféré à un IDE graphique (contrainte ressources ENV2)

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier `.db` ou `.sqlite` sur ENV2 |
| `mode` | enum | ❌ | `read` / `inspect` / `wal-stats` (défaut: `read`) |
| `max_rows` | integer | ❌ | Nombre max de lignes à afficher par table (défaut: 50) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables` | array | Liste des tables avec nombre de lignes et taille |
| `wal_size` | integer | Taille du fichier WAL associé (octets) |
| `schema` | object | Schéma des tables explorées |
| `sample_rows` | array | Exemples de lignes par table |
| `evidence_hash` | string | Hash SHA-256 de l'exploration |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est un chemin absolu explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier .db / .sqlite sur ENV2
→ Vérifier que le fichier est lisible (permissions)
```

### Étape 2 — Lancement du TUI SQLite

```
→ Lancer le binaire sqlite-tui (Pastalikek65) en mode lecture seule
→ Afficher les tables, le nombre de lignes et la taille WAL
→ Capturer la sortie brute du terminal (stdout)
```

### Étape 3 — Preuve d'exécution

```
→ Calculer le hash SHA-256 de la sortie brute
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base (mode lecture seule)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un client graphique lourd sur ENV2 (viole la contrainte ressources legacy)
- ❌ Écrire dans la base pendant l'exploration (risque de corruption WAL)
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600 (contraintes hardware ENV2)
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
