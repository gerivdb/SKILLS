---
name: antigravity-gemini-extension
description: Extension liée aux workflows Antigravity / Gemini et à l'interaction navigateur/CDP. Pattern inspiré de https://github.com/lucasmartins-ai/antigravity-gemini-extension
version: 1.0.0
intent_hash: 0xSKILL_ANTIGRAVITY_GEMINI_EXTENSION_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/lucasmartins-ai/antigravity-gemini-extension
source_url: https://github.com/lucasmartins-ai/antigravity-gemini-extension
path: antigravity-gemini-extension
---

# Antigravity Gemini Extension — Skill KiloCode

## Objectif

Fournir une référence canonique pour l'extension liée aux workflows Antigravity / Gemini et à l'interaction navigateur/CDP. Adapté à ENV2 pour l'orchestration des interactions entre agents Antigravity, Gemini et le navigateur via CDP (port 9222, Profil 2).

## Déclencheur

Ce skill s'active quand :
- Il faut orchestrer des interactions entre Antigravity, Gemini et un navigateur
- L'extension CDP doit être utilisée pour piloter le navigateur (port 9222, Profil 2)
- Des workflows Antigravity/Gemini doivent être exécutés sur ENV2
- L'interaction navigateur doit respecter les règles BDCP (CDP uniquement, pas de réseau direct)

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `cdp_port` | integer | ✅ | Port CDP du navigateur (défaut: 9222) |
| `profile` | string | ✅ | Profil Chromium à utiliser (défaut: Profil 2) |
| `workflow_type` | enum | ✅ | `antigravity` / `gemini` / `hybrid` |
| `target_url` | string | ❌ | URL cible dans le navigateur |
| `action` | string | ❌ | Action à exécuter (inject, send, read, etc.) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `cdp_session_id` | string | ID de la session CDP établie |
| `action_result` | string | Résultat de l'action exécutée |
| `workflow_executed` | string | Type de workflow exécuté |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du profil CDP

```
→ Vérifier que le port CDP 9222 est actif (http://127.0.0.1:9222/json/version)
→ Confirmer que le Profil 2 Chromium est utilisé (règle chromium-runtime-invariants)
```

### Étape 2 — Exécution du workflow

```
→ Attacher l'extension Antigravity/Gemini à la session CDP
→ Exécuter l'action demandée (inject, send, read) selon le workflow_type
→ Respecter les règles BDCP (pas de réseau direct, CDP uniquement)
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier que la session CDP est propre après exécution
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un profil Chromium temporaire au lieu du Profil 2 (règle chromium-runtime-invariants)
- ❌ Effectuer des requêtes réseau directes au lieu de passer par le CDP (règle BDCP)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la règle DOM Empiricism (pas de sélecteur supposé sans preuve CDP)

## Référence ADR

- **ADR** : ADR-2026-11-20-001-CHROMIUM-EXTENSION-LIFECYCLE-HMR
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : chromium-runtime-invariants
- **Règle** : rule-dom-empiricism
