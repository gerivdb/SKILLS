# Pattern Local Bridge Guard — Extensions dépendantes d'un daemon local

## Objectif

Éviter qu'une extension Chromium ne promeuve l'absence d'un daemon local (pont 8810, relais 19988, passerelle 8796, etc.) en une **erreur fatale rouge** dans le Service Worker. L'indisponibilité d'un service local est un **état d'infrastructure transitoire**, pas un bug applicatif.

## Règle d'or

> **Fail-silent, pas de polling réseau aveugle sans vérification préalable.**

Toute extension qui s'appuie sur un daemon local DOIT :
1. **Sonder la disponibilité du port** avant toute tentative de connexion WebSocket/TCP.
2. **Basculer en état STANDBY silencieux** si le démon n'est pas démarré (aucun `console.error`, aucun badge rouge).
3. **Ne tenter la connexion que sur commande explicite utilisateur** ou présence avérée du démon.

## Application à `browse` (port 19988)

Dans `C:\Temp\OpenCode_Fork\dist\background.js` :
- L'appel `new WebSocket("ws://127.0.0.1:19988/extension")` est conditionné à l'activation explicite du mode agent local.
- Le démarrage automatique `Se("startup")` a été neutralisé (remplacé par un no-op).
- L'onboarding intempestif `onboarding.html?first-run` a été neutralisé.

## Application à `DEEP-X` / `GEM-X` (pont 8810)

Le pont 8810 doit être sondé avant toute tentative de `fetch`/`XMLHttpRequest`. Si le port ne répond pas, l'extension reste en mode dégradé silencieux.

## Intégration Cockpit CDP

Le script `chromium_cdp_cockpit.py` fournit :
- `status` — détection des extensions actives et de leurs erreurs
- `clear-errors` — purge du journal d'erreurs Chromium
- `audit` — matrice de santé globale (nom, version, statut, statut santé)

Toute modification d'extension dépendante d'un daemon local doit être suivie de :
1. `reload --id <ID>` (après activation si nécessaire)
2. `clear-errors --id <ID>`
3. `status` → vérifier `hasErrors: false`

## Référence ADR

- **ADR** : `ADR-2026-11-20-001-CHROMIUM-EXTENSION-LIFECYCLE-HMR.md`
- **IntentHash** : `0xCHROMIUM_EXTENSION_LIFECYCLE_HMR_20261120`
