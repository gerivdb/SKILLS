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
- **React-aware** : le remplissage d'un champ de saisie React **NE DOIT PAS** utiliser `.value =` (contourne le value tracker, le composant ne voit pas le texte). Utiliser impérativement `page.keyboard.type()` ou `Input.insertText` via CDP, qui déclenche `onChange` et rend le bouton d'envoi.
- **Sélecteurs de rôle** : le DOM DeepSeek utilise des classes CSS, pas d'attribut `data-message-author-role`. Le bouton d'envoi est conditionnel (rendu quand le texte est non vide). Les blocs de message utilisateur utilisent `.fa81`, les blocs assistant utilisent `[class*="f9bf"]`.

## Entrées / dépendances
- CDP `http://127.0.0.1:9222/json/version`, `/json/list` (targets page DeepSeek).
- Tab cible : `https://chat.deepseek.com/...` (session active, AUTH_OK).
- Citizen/daemon : `shard-f-synaptic-gateway` (hybrid v4 + frontmatter).

## Comportement
1. **Discovery** : lister targets, sélectionner la page DeepSeek contrôlable (WS `devtools/page/<id>`).
2. **no_tab** : si aucune page DeepSeek valide → état `no_tab`, émettre alerte/évidence, ne pas tenter de lancer Chrome ; demander routage HITL si nécessaire.
3. **Envoi** : `page.keyboard.type(message, delay=50)` dans la textarea (placeholder "Message" ou `#chat-input`), puis déclencher le bouton d'envoi (`button[aria-label*="Send" i]`) ou `Enter`.
4. **Résilience** : retry borné, heartbeat `shard_f`, WAL/ledger append-only selon pipeline existant.
5. **Assertion** : jamais d'assertion `includes()` sur le contenu brut. Regex d'ancrage `^\[ENV6\]\s+ACK\s+` et filtre par rôle (blocs assistant uniquement, `.f9bf7997` / `[class*="f9bf"]`).

## Critères de succès
- Message livré sur session DeepSeek authentifiée, preuve (evidence + ledger) produite.
- Aucune tentative de lancement navigateur.
- L'ACK ENV6, quand il est produit, est détecté exclusivement dans un bloc assistant via le motif `[ENV6] ACK <token>` en début de ligne.

## Observabilité
- `e2e_output/.heartbeat/shard_f`, `f_daemon_frontmatter_evidence.json`, ledger/WAL 0x243.
- `scripts/verify_ack_e2e.py` : preuve d'acquittement avec hash SHA-256 et timestamp UTC.