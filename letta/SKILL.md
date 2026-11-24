---
name: letta
description: Plateforme d'agents avec mémoire hiérarchisée et gestion d'états persistants. Pattern inspiré de https://github.com/letta-ai/letta
version: 1.0.0
intent_hash: 0xSKILL_LETTA_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/letta-ai/letta
source_url: https://github.com/letta-ai/letta
path: letta
---

# Letta — Skill KiloCode

## Objectif

Fournir une référence canonique pour Letta, plateforme d'agents avec mémoire hiérarchisée et gestion d'états persistants. Adapté à ENV2 pour la gestion d'agents avec mémoire persistante locale sans dépendance cloud.

## Déclencheur

Ce skill s'active quand :
- Il faut gérer un agent avec mémoire hiérarchisée sur ENV2
- Des états persistants doivent être maintenus entre les sessions
- La mémoire doit être organisée de manière hiérarchique (court terme, long terme, procédural)
- L'environnement ENV2 nécessite une plateforme d'agent locale et souveraine

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `agent_id` | string | ✅ | Identifiant de l'agent |
| `state_path` | string | ✅ | Chemin absolu vers le fichier d'état persistant |
| `memory_layer` | enum | ❌ | `short_term` / `long_term` / `procedural` / `all` (défaut: `all`) |
| `action` | enum | ✅ | `read` / `write` / `update` / `delete` |
| `content` | string | ❌ | Contenu à écrire/mettre à jour dans la mémoire |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `state_loaded` | boolean | True si l'état a été chargé |
| `memory_content` | array | Contenu de la mémoire par couche |
| `state_updated` | boolean | True si l'état a été mis à jour |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que state_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier d'état sur ENV2
```

### Étape 2 — Gestion de la mémoire

```
→ Charger l'état de l'agent depuis state_path
→ Selon l'action : lire, écrire, mettre à jour ou supprimer la mémoire
→ Organiser selon la mémoire_layer demandée
→ Sauvegarder l'état mis à jour si nécessaire
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité du fichier d'état après l'opération
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser une plateforme d'agent cloud externe au lieu de Letta local sur ENV2
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte disque ENV2 pour les états persistants

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
