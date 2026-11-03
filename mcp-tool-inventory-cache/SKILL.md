---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_MTIC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/mcp-tool-inventory-cache/SKILL.md
---

# Skill - mcp-tool-inventory-cache

## Objectif

Met en cache les outils decouverts pour repondre instantanement a tools/list sans interroger les processus a froid. Ameliore la latence du gateway MCP pour les clients qui listent les outils disponibles.

## Declencheur

- Premier appel a tools/list sur un backend MCP.
- Invalidation du cache suite a changement de configuration backend.
- Requete repetee de tools/list sur le meme backend.

## Entrees

- Identifiant du backend MCP.
- Liste des outils declares par le backend.
- TTL du cache (en secondes, par defaut 300).

## Sorties

- Liste des outils en cache (nom, description, inputSchema).
- Statut du cache (hit / miss / expire).
- Code retour 0 si cache disponible, 1 si interrogation froide requise.

## Regles Operationnelles

### 1. Mise en cache des outils decouverts
Lors du premier appel a tools/list, les outils sont mises en cache avec leur TTL.

### 2. Reponse depuis le cache
Les appels subsequents a tools/list repondent depuis le cache sans interroger le processus backend.

### 3. Invalidation du cache
Le cache est invalide si la configuration du backend change ou si le TTL expire.

### 4. Fallback sur interrogation froide
Si le cache est expire ou vide, une interrogation froide du backend est effectuee et le cache est mis a jour.

### 5. Journalisation
Chaque hit ou miss de cache est consigne avec le backend et l'horodatage.
