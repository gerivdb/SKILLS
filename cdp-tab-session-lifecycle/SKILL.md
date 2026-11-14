---
name: cdp-tab-session-lifecycle
description: Cycle de vie onglet CDP (attach-only REF-216) — ouverture, stabilité, fermeture propre, gestion NO_TAB/AUTH_REDIRECT/TARGET_GONE avec evidence.
---
# cdp-tab-session-lifecycle

Gestion du cycle de vie des onglets via **Chrome DevTools Protocol** en mode **attach-only** (`127.0.0.1:9222`, REF-216). **Jamais de lancement Chrome/Chromium.**

## Contraintes
- Clone CDP actif requis (voir `profile-manager-cockpit` / `chrome-profile-manager-master-to-clone`). Aucune création de profil ni launch navigateur.
- Validation auth/session chaînée avec `deepseek-auth-state-validator` quand la cible est DeepSeek.

## Opérations
1. **Ouverture d’onglet**
   - HTTP (préféré, simple) : `PUT http://127.0.0.1:9222/json/new?url=<encoded>` (ou variante `?`/endpoint selon build ; fallback `Target.createTarget` via WS).
   - WS : `Target.createTarget` avec `url`.
2. **Attente de stabilité** (équivalent `networkidle`)
   - Polling `/json/list` jusqu’à présence du `targetId`/page attendu.
   - Probe readiness : `Runtime.evaluate` → `document.readyState` (`interactive`/`complete`) + stabilité courte (pas de navigation en cours) avec timeout borné.
3. **Fermeture propre**
   - HTTP : `PUT http://127.0.0.1:9222/json/close/<targetId>` (ou `/json/close?targetId=`), fallback WS `Target.closeTarget`.

## Gestion des erreurs / états
- `NO_TAB` : aucun onglet cible contrôlable → tenter ouverture (si clone actif) ou signaler.
- `AUTH_REDIRECT` : URL/page redirigée vers `/sign_in` → état auth requis (HITL credentials), ne pas automatiser le login.
- `TARGET_GONE` : target disparu en cours d’opération → resnapshot `/json/list`, retry borné puis échec explicite.

## Evidence & logging
- Capturer snapshot `/json/list` **avant/après** chaque action (open/close/switch) avec horodatage.
- Sur échec critique (impossible d’ouvrir/fermer, boucle redirect, target instable) : consigner un bloc dans `HITL_PENDING.md` (contexte, target, URL, état, action tentée) — append-only.
- Heartbeats/WAL du flux appelant inchangés (ne pas modifier ledger destructivement).

## Garde-fous
- Attach-only strict, pas de relance navigateur. Timeouts/retries bornés. Pas d’action destructive hors périmètre.