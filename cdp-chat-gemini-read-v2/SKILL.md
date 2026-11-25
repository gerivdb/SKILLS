# M3 Skill — CDP Chat Gemini Read v2
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 2.0
IntentHash: 0xM3_SKILL_CDP_CHAT_GEMINI_READ_V2_20261125

## Définition
Lecture de la réponse assistant du chat Gemini via CDP (port 9222, Profil 2).
Utilise le sélecteur DOM actuel de Gemini : `div.markdown-main-panel.md-content`.
Remplace le skill v1 qui utilisait le sélecteur obsolète `.message-text`.
Utilise du polling avec détection de stabilité pour capturer la réponse complète.

## Source
- Sélecteur DOM validé : `div.markdown-main-panel.md-content` (vérifié par dump DOM CDP le 2026-11-25)
- Sélecteur précédent (obsolète) : `.message-text` (ne correspond plus à la structure DOM actuelle de Gemini)

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Python avec modules websocket, urllib.request
- Onglet Gemini ouvert avec une conversation en cours

## GESTES (séquence atomique)

### GESTE-1 — Préflight CDP
```
GET http://127.0.0.1:9222/json/version
→ Vérifier que le port CDP répond
```

### GESTE-2 — Trouver l'onglet Gemini
```
GET http://127.0.0.1:9222/json/list
→ Filtrer: url contient gemini.google.com
→ Récupérer webSocketDebuggerUrl
```

### GESTE-3 — Connexion WebSocket + Runtime.enable
```
WS connect: ws://127.0.0.1:9222/devtools/page/<target_id>
CDP: Runtime.enable
CDP: Page.enable
```

### GESTE-4 — Lire les réponses assistant avec sélecteur actuel
```
CDP: Runtime.evaluate
expression: (() => {
  const els = document.querySelectorAll('div.markdown-main-panel.md-content');
  if (els.length === 0) return 'no_elements';
  const last = els[els.length - 1];
  return last.innerText.trim();
})()
returnByValue: true
```

### GESTE-5 — Polling avec détection de stabilité
```
Répéter GESTE-4 jusqu'à stabilité :
- Comparer la longueur du texte avec le poll précédent
- Si identique sur 2 polls consécutifs → stabilité atteinte
- Timeout maximal: 120 secondes
- Intervalle entre polls: 1000 ms
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| cdp_tab_id | string (optionnel) | ID de l'onglet CDP cible (défaut: auto-détection) |
| timeout_sec | integer | Timeout maximal en secondes (défaut: 120) |
| poll_interval_ms | integer | Intervalle entre polls en ms (défaut: 1000) |
| stability_polls | integer | Nombre de polls consécutifs identiques (défaut: 2) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "cdp-chat-gemini-read-v2",
  "playground": "gemini",
  "selector": "div.markdown-main-panel.md-content",
  "response": "<texte de la réponse assistant>",
  "response_length": N,
  "sha256_response": "<hash>",
  "stability_polls": 2,
  "timestamp_utc": "2026-11-25T01:XX:XXZ",
  "cdp_tab_id": "<tab_id>"
}
```

## Règles d'or
- Sélecteur DOM actuel de Gemini (pas de sélecteur obsolète)
- Hash SHA-256 de la réponse enregistré pour preuve d'intégrité
- Détection de stabilité: le texte ne change plus sur 2 polls consécutifs
- Aucun envoi réseau direct, tout passe par CDP
- Respecte la règle DOM Empiricism: sélecteur vérifié par dump DOM préalable

## Preuve d'exécution
- Horodatage UTC au moment de la lecture
- Hash SHA-256 de la réponse lue
- ID de l'onglet CDP
- Nombre de polls de stabilité

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-chat-gemini-read-v2\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-chat-gemini-read-v2\impl\cdp_chat_gemini_read_v2.py` |

## Hash de ce skill
Horodatage: 2026-11-25T01:XX:XXZ | WAL: 0x243 | IntentHash: 0xM3_SKILL_CDP_CHAT_GEMINI_READ_V2_20261125
