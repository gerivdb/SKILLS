---
name: deepseek-synaptic-gateway-cdp
description: Gateway synaptique DeepSeek via CDP (attach-only 9222). Envoie/route des messages vers l'UI DeepSeek sans lancer Chrome (REF-216), gère l'absence d'onglet (no_tab) et les états de session/auth.
---
# deepseek-synaptic-gateway-cdp

## Rôle
Pont ENV6↔DeepSeek via **Chrome DevTools Protocol** en mode **attach-only** sur `127.0.0.1:9222`. Ne jamais démarrer/relancer Chromium/Chrome.

## Contraintes (REF-216, HOTL)
- **Attach-only** : se connecter uniquement à une instance debug déjà exposée (`--remote-debugging-port=9222`).
- **Interdit** : `chrome.exe`/`chromium` launch, création de profil, modification destructive de session.
- **HITL requis** : ouverture manuelle de Chrome/profil, login DeepSeek, résolution d'incidents credentials.

## Entrées / dépendances
- CDP `http://127.0.0.1:9222/json/version`, `/json/list` (targets page DeepSeek).
- Tab cible : `https://chat.deepseek.com/...` (session active, AUTH_OK).
- Citizen/daemon : `shard-f-synaptic-gateway` (hybrid v4 + frontmatter).

## Comportement
1. **Discovery** : lister targets, sélectionner la page DeepSeek contrôlable (WS `devtools/page/<id>`).
2. **no_tab** : si aucune page DeepSeek valide → état `no_tab`, émettre alerte/évidence, ne pas tenter de lancer Chrome ; demander routage HITL si nécessaire.
3. **Envoi** : injection DOM/CDP (textarea/send) selon contrat UI, avec evidence JSON (ok, session_id, http/auth signals).
4. **Résilience** : retry borné, heartbeat `shard_f`, WAL/ledger append-only selon pipeline existant.

## Critères de succès
- Message livré sur session DeepSeek authentifiée, preuve (evidence + ledger) produite.
- Aucune tentative de lancement navigateur.

## Observabilité
- `e2e_output/.heartbeat/shard_f`, `f_daemon_frontmatter_evidence.json`, ledger/WAL 0x243.
