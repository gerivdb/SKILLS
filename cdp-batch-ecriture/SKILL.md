# M3 Skill — CDP Batch Écriture
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_CDP_BATCH_ECRITURE_20261125

## Définition
Enchaîne injection de prompt et clic "Envoyer" sur Chromium/Gemini via une seule connexion WebSocket CDP persistante. Remplace les 2 opérations séparées (inject puis send) par un batch atomique sur un tunnel unique.

## Problème traité
Actuellement : inject et send sont 2 compétences distinctes, chacune ouvrant sa propre connexion WebSocket avec Page.enable + Runtime.enable. Le batch réduit à 1 connexion WebSocket pour les 2 opérations.

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Python avec modules websocket, urllib.request
- Onglet Gemini ouvert avec zone de saisie visible

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
```

### GESTE-4 — Injection + Clic en batch
```
CDP: Runtime.evaluate (inject prompt)
CDP: Runtime.evaluate (clic bouton Envoyer)
→ Les 2 commandes sur la même connexion WebSocket
```

### GESTE-5 — Fermeture du tunnel
```
WS close
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| prompt | string | Texte à injecter dans la zone de saisie Gemini |
| cdp_tab_id | string (optionnel) | ID de l'onglet CDP cible |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "cdp-batch-ecriture",
  "playground": "gemini",
  "inject_result": "...",
  "send_result": "clicked",
  "connections_used": 1,
  "connections_saved": 1,
  "latency_ms": N,
  "timestamp_utc": "...",
  "cdp_tab_id": "..."
}
```

## Règles d'or
- 1 connexion WebSocket pour inject + send (au lieu de 2)
- Page.enable et Runtime.enable appelés une seule fois
- Pas de script inline ad hoc : exécution via le skill canonique

## Preuve d'exécution
- Horodatage UTC
- Latence mesurée en ms
- Nombre de connexions WebSocket économisées

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-batch-ecriture\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-batch-ecriture\impl\cdp_batch_ecriture.py` |

## Hash de ce skill
Horodatage: 2026-11-25T02:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_CDP_BATCH_ECRITURE_20261125
