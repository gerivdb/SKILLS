---
name: deepseek-auth-state-validator
description: Validation des états d’auth/session DeepSeek (AUTH_OK/REQUIRED/UNKNOWN/NO_DEEPSEEK_TARGET/NO_TOKEN) et décisions HOTL associées.
---
# deepseek-auth-state-validator

Normalise l’état d’authentification DeepSeek via CDP/clone et déclenche les actions sûres.

## États normalisés
- `AUTH_OK` : messages > 0 **et** `sessionId` présent.
- `AUTH_REQUIRED` : redirection/présence `/sign_in`.
- `AUTH_UNKNOWN` : `rawToken`/cookie présent mais `sessionId` null (session non matérialisée).
- `NO_DEEPSEEK_TARGET` : aucun onglet DeepSeek dans `/json/list`.
- `NO_TOKEN` : aucun cookie/token exploitable.

## Commande canonique
```powershell
python e2e_output/validate_deepseek_auth.py
```
Parser `RC` et le code/état émis (stdout/stderr) pour décider.

## Décision HOTL
- `AUTH_OK` → continuer le flux.
- `AUTH_REQUIRED` → **HITL** (credentials humains, seul cas légitime). Logger dans `HITL_PENDING.md`.
- `AUTH_UNKNOWN` → déclencher `cdp-tab-session-lifecycle` (ouvrir/naviguer une conversation) pour matérialiser le `sessionId`, puis revalider.
- `NO_DEEPSEEK_TARGET` → `cdp-tab-session-lifecycle` (ouvrir onglet DeepSeek sur clone actif).
- `NO_TOKEN` → vérifier profil/clone (Pattern A) ; si toujours absent → **HITL**.

## Logging
- `HITL_PENDING.md` uniquement pour `AUTH_REQUIRED` / `NO_TOKEN` (append-only, contexte minimal).
- Les autres transitions restent en evidence runtime standard.

## Garde-fous
- Attach-only REF-216, pas de saisie/stockage de credentials par l’agent, pas de launch Chrome.