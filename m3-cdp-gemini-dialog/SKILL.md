# M3 Skill — Dialogue CDP ENV2 → Gemini via Profil 2
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_CDP_GEMINI_DIALOG_20261122

## Définition
Primitive de compétence atomique pour établir un canal CDP (Chrome DevTools Protocol) entre ENV2 (station HP Z600) et ENV3 (Google Gemini) via le vrai Profil 2 de Chromium (port 9222), authentifié, sans Playwright, sans polling excessif, avec preuve de livraison.

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Onglet Gemini ouvert dans le Profil 2
- Python avec module websockets installé sur ENV2

## Sélecteurs DOM validés (preuve CDP)

| Élément | Sélecteur CSS | Statut |
|---------|--------------|--------|
| Champ de saisie | `div[aria-label="Saisissez un prompt pour Gemini"]` | ✅ Validé (contenteditable) |
| Envoi | `Input.dispatchKeyEvent` key=Enter | ✅ Validé (champ vidé après envoi) |
| Réponse Gemini | `div.response-content` | ✅ Validé |
| Réponse Gemini (alt) | `div.markdown.markdown-main-panel` | ✅ Validé |

## Gestes (séquence atomique)

### GESTE-1 — Vérifier le port CDP
```
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 3
```
Résultat attendu : JSON avec `webSocketDebuggerUrl`.

### GESTE-2 — Lister les onglets et trouver Gemini
```
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/list" -TimeoutSec 5
```
Filtrer : `title` contient "Gemini" ou `url` contient `gemini.google.com`.
Extraire : `id` et `webSocketDebuggerUrl`.

### GESTE-3 — Naviguer vers nouvelle conversation
CDP `Page.navigate` vers `https://gemini.google.com/app` sur le WebSocket de l'onglet cible.

### GESTE-4 — Activer Runtime
```json
{"id": 1, "method": "Runtime.enable"}
```

### GESTE-5 — Écrire dans le champ de saisie
```javascript
(function(){
  const el = document.querySelector('div[aria-label="Saisissez un prompt pour Gemini"]');
  if (el) {
    el.focus();
    el.textContent = '<MESSAGE>';
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return "WRITE_OK";
  }
  return "WRITE_ERR";
})()
```

### GESTE-6 — Envoyer (Entrée clavier)
```json
{"id": 4, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}}
{"id": 5, "method": "Input.dispatchKeyEvent", "params": {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13}}
```

### GESTE-7 — Vérifier l'envoi
```javascript
(function(){
  const el = document.querySelector('div[aria-label="Saisissez un prompt pour Gemini"]');
  return el ? el.textContent : "NOT_FOUND";
})()
```
Résultat attendu : `""` (champ vidé = message envoyé).

### GESTE-8 — Lire la réponse Gemini
```javascript
(function(){
  const el = document.querySelector('div.response-content');
  return el ? el.textContent : "NOT_FOUND";
})()
```

## Règles d'or
- DOM Empiricism : jamais de sélecteur CSS supposé sans preuve CDP préalable
- Verbatim Fidelity : restitution textuelle entre triple backticks + hash SHA-256
- Win32 Hidden Window : aucune fenêtre console visible pour les appels natifs
- Pas de Playwright : CDP natif (WebSocket direct) uniquement
- Une injection par tour, attendre la réponse via lecture DOM
- BDCP : clapet fermé par défaut, ne jamais ouvrir sans ordre explicite utilisateur

## Preuve d'exécution (cette session)
- Date/heure : 2026-11-22T23:35:00Z
- Port CDP : 9222 (127.0.0.1)
- Navigateur : Chrome/147.0.7727.55
- Profil : Profile 2 (authentifié)
- Onglet Gemini : E971A7568E2CFAED50C869DE7FAC9E6B
- Message envoyé : "Test de canal CDP ENV2 vers Gemini - nouvelle conversation via Profil 2 authentifié. Vérification de connexion."
- Réponse reçue : ✅ Texte complet extrait de `div.response-content`
- Statut : Canal CDP ENV2 → Gemini opérationnel

## Fichiers associés sur disque
| Fichier | Chemin absolu |
|---------|--------------|
| Client CDP Profil 2 | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2\chromium_cdp_client.py` |
| Lanceur Profil 2 | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-extension-cockpit\scripts\launch_profile2.ps1` |
| Index CDP Profil 2 | `D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\INDEX_CDP_PROFIL2.md` |
| Ontologie Skill CDP | `D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY\concepts\m3-skill-cdp-env3-communication.md` |
| Ontologie Citizen CDP | `D:\DO\WEB\TOOLS\L0-CANON\ONTOLOGY\concepts\m3-citizen-env2-cdp-relay.md` |

## Hash de ce skill
Horodatage: 2026-11-22T23:39:00Z | WAL: 0x243 | IntentHash: 0xM3_SKILL_CDP_GEMINI_DIALOG_20261122