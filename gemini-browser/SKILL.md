---
name: gemini-browser
description: Exemple open source d'agent navigateur piloté avec Gemini. Pattern inspiré de https://github.com/browserbase/gemini-browser
version: 1.0.0
intent_hash: 0xSKILL_GEMINI_BROWSER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/browserbase/gemini-browser
source_url: https://github.com/browserbase/gemini-browser
path: gemini-browser
---

# Gemini Browser — Skill KiloCode

## Objectif

Fournir une référence canonique pour un agent navigateur piloté avec Gemini. Adapté à ENV2 pour l'automatisation de navigateur via CDP avec Gemini comme moteur de décision, en respectant les règles BDCP et DOM Empiricism.

## Déclencheur

Ce skill s'active quand :
- Il faut piloter un navigateur via Gemini et CDP sur ENV2
- Des actions de navigateur doivent être orchestrées par un LLM (Gemini)
- L'interaction doit respecter les règles BDCP (port 9222, Profil 2, pas de réseau direct)
- Le DOM doit être vérifié empiriquement avant toute sélection d'élément

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `cdp_port` | integer | ✅ | Port CDP du navigateur (défaut: 9222) |
| `profile` | string | ✅ | Profil Chromium (défaut: Profil 2) |
| `target_url` | string | ✅ | URL cible à charger dans le navigateur |
| `gemini_action` | string | ✅ | Action à demander à Gemini (clic, saisie, extraction, etc.) |
| `selector_proof` | boolean | ❌ | Vérifier le sélecteur via DOM Empiricism avant action (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `browser_session_id` | string | ID de la session navigateur |
| `gemini_response` | string | Réponse de Gemini pour l'action demandée |
| `dom_verified` | boolean | True si le sélecteur a été vérifié via CDP |
| `action_result` | string | Résultat de l'action exécutée |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification CDP et Profil

```
→ Vérifier http://127.0.0.1:9222/json/version (CDP actif)
→ Confirmer l'utilisation du Profil 2 Chromium (règle chromium-runtime-invariants)
```

### Étape 2 — Vérification DOM (DOM Empiricism)

```
→ Avant toute sélection d'élément, dumper le DOM cible via CDP
→ Vérifier que le sélecteur existe réellement dans le DOM
→ Ne jamais présumer l'existence d'un attribut (data-testid, aria-label, etc.)
```

### Étape 3 — Exécution via Gemini

```
→ Envoyer l'action à Gemini via CDP
→ Exécuter l'action dans le navigateur
→ Respecter les règles BDCP (pas de réseau direct)
```

### Étape 4 — Preuve d'exécution

```
→ Capturer la réponse de Gemini et le résultat de l'action
→ Calculer le hash SHA-256 du résultat complet
→ Enregistrer l'horodatage UTC
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un sélecteur CSS sans vérification DOM préalable (viole DOM Empiricism)
- ❌ Utiliser un profil Chromium temporaire (viole chromium-runtime-invariants)
- ❌ Effectuer des requêtes réseau directes (viole BDCP)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-11-20-001-CHROMIUM-EXTENSION-LIFECYCLE-HMR
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : chromium-runtime-invariants
- **Règle** : rule-dom-empiricism
- **Règle** : bdcp-kiva-workflow
