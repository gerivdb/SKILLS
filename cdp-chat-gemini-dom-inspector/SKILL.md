# M3 Skill — CDP Chat Gemini DOM Inspector
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_CDP_CHAT_GEMINI_DOM_INSPECTOR_20261124

## Définition
Inspection du DOM de l'onglet Gemini via CDP (port 9222, Profil 2) pour découvrir les sélecteurs CSS réels des messages assistant. Dump les éléments candidates (rôles, classes, attributs data-*) pour mise à jour de la base chat-playground-ui.db.

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Python avec modules websocket, urllib.request
- Onglet Gemini ouvert sur https://gemini.google.com/app

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

### GESTE-4 — Dump des éléments candidats "message assistant"
```
CDP: Runtime.evaluate
expression: (() => {
  const candidates = [];
  // Chercher par rôle
  document.querySelectorAll('[role]').forEach(el => {
    const role = el.getAttribute('role');
    if (role && (role.includes('assistant') || role.includes('article') || role.includes('region'))) {
      candidates.push({
        tag: el.tagName,
        role: role,
        class: el.className,
        'aria-label': el.getAttribute('aria-label'),
        'data-message-author-role': el.getAttribute('data-message-author-role'),
        innerText: el.innerText ? el.innerText.substring(0, 100) : null,
        children: el.children.length
      });
    }
  });
  // Chercher par classe contenant 'message' ou 'assistant'
  document.querySelectorAll('[class*="message"], [class*="assistant"], [class*="model"]').forEach(el => {
    if (!candidates.some(c => c.tag === el.tagName && c.class === el.className)) {
      candidates.push({
        tag: el.tagName,
        role: el.getAttribute('role'),
        class: el.className,
        'aria-label': el.getAttribute('aria-label'),
        'data-message-author-role': el.getAttribute('data-message-author-role'),
        innerText: el.innerText ? el.innerText.substring(0, 100) : null,
        children: el.children.length
      });
    }
  });
  return candidates.slice(0, 50);
})()
returnByValue: true
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| cdp_tab_id | string (optionnel) | ID de l'onglet CDP cible (défaut: auto-détection) |
| max_elements | integer | Nombre max d'éléments à retourner (défaut: 50) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "cdp-chat-gemini-dom-inspector",
  "playground": "gemini",
  "elements": [ { "tag", "role", "class", "aria-label", "data-message-author-role", "innerText", "children" } ],
  "element_count": N,
  "timestamp_utc": "...",
  "cdp_tab_id": "..."
}
```

## Règles d'or
- Aucun envoi réseau direct, tout passe par CDP
- Hash SHA-256 du DOM dump enregistré pour preuve d'intégrité
- Ne jamais présumer l'existence d'un attribut sans vérification DOM (règle DOM Empiricism)

## Preuve d'exécution
- Horodatage UTC au moment de l'inspection
- Nombre d'éléments trouvés
- ID de l'onglet CDP

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-chat-gemini-dom-inspector\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-chat-gemini-dom-inspector\impl\cdp_chat_gemini_dom_inspector.py` |

## Hash de ce skill
Horodatage: 2026-11-25T00:XX:XXZ | WAL: 0x243 | IntentHash: 0xM3_SKILL_CDP_CHAT_GEMINI_DOM_INSPECTOR_20261124
