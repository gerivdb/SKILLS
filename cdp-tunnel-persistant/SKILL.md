# M3 Skill — CDP Tunnel Persistant
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_CDP_TUNNEL_PERSISTANT_20261125

## Définition
Établit et maintient une connexion WebSocket CDP persistante (port 9222, Profil 2) pour éliminer le barrage de réouverture de connexion à chaque opération d'écriture sur Chromium. Remplace les 3 connexions WebSocket séparées (inject/send/read) par un tunnel unique réutilisable.

## Problème traité
Actuellement : 1 connexion WebSocket par opération (inject + send + read = 3 connexions, 3× Page.enable + 3× Runtime.enable, 3 fermetures). Goulot d'étranglement réseau et latence cumulée.

## Solution
Une connexion WebSocket CDP unique, maintenue ouverte, sur laquelle les commandes Runtime.evaluate sont envoyées séquentiellement sans réouverture. Économie : 2 connexions WebSocket et 4 appels d'initialisation (Page.enable/Runtime.enable) par cycle d'écriture.

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

### GESTE-3 — Ouvrir le tunnel WebSocket persistant
```
WS connect: ws://127.0.0.1:9222/devtools/page/<target_id>
CDP: Runtime.enable (une seule fois)
CDP: Page.enable (une seule fois)
→ La connexion reste ouverte pour les opérations suivantes
```

### GESTE-4 — Exécuter des commandes sur le tunnel
```
CDP: Runtime.evaluate (inject)
CDP: Runtime.evaluate (clic send)
CDP: Runtime.evaluate (lecture réponse)
→ Toutes sur la même connexion WebSocket
```

### GESTE-5 — Fermeture propre du tunnel
```
WS close (uniquement après la dernière opération)
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| cdp_tab_id | string (optionnel) | ID de l'onglet CDP cible |
| keep_alive | boolean | Maintenir la connexion ouverte après l'opération (défaut: true) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "cdp-tunnel-persistant",
  "playground": "gemini",
  "websocket_opened": true,
  "commands_executed": N,
  "connections_saved": 2,
  "timestamp_utc": "...",
  "cdp_tab_id": "..."
}
```

## Règles d'or
- Une seule connexion WebSocket par session d'écriture
- Page.enable et Runtime.enable appelés une seule fois
- Fermeture propre du tunnel après la dernière opération
- Aucun envoi réseau direct, tout passe par CDP

## Preuve d'exécution
- Horodatage UTC
- Nombre de connexions WebSocket économisées
- ID de l'onglet CDP

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-tunnel-persistant\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-tunnel-persistant\impl\cdp_tunnel_persistant.py` |

## Hash de ce skill
Horodatage: 2026-11-25T02:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_CDP_TUNNEL_PERSISTANT_20261125
