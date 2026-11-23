# M3 Skill — CDP Preflight Sentinel
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xM3_SKILL_CDP_PREFLIGHT_SENTINEL_20261123

## Définition
Sentinel preflight qui valide la connectivité CDP (port 9222, Runtime.enable, Runtime.evaluate) en moins de 2 secondes avant tout envoi vers Gemini ou DeepSeek. Évite les envois vers cible inaccessible.

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Python avec modules websockets, urllib

## GESTES (séquence atomique, < 2s total)

### GESTE-1 — Vérifier port CDP HTTP
```
GET http://127.0.0.1:9222/json/version
Timeout: 2s
Résultat attendu: JSON avec webSocketDebuggerUrl
```

### GESTE-2 — Lister onglets et trouver cible
```
GET http://127.0.0.1:9222/json/list
Timeout: 2s
Filtrer: title contient "Gemini" ou "DeepSeek" ou url contient gemini.google.com / chat.deepseek.com
```

### GESTE-3 — Connexion WebSocket + Runtime.enable + Evaluate test
```
WS connect: ws://127.0.0.1:9222/devtools/page/<target_id>
Timeout: 1s

CDP: Runtime.enable → réponse attendue {"id":1,"result":{}}
CDP: Runtime.evaluate {"expression":"'preflight_ok'","returnByValue":true}
→ réponse attendue {"result":{"result":{"type":"string","value":"preflight_ok"}}}
```

### GESTE-4 — Décision
- Tous gestes OK en < 2s → return {"ok": true, "latency_ms": N}
- Échec quelconque → return {"ok": false, "error": "description", "stage": "port|tabs|ws|runtime|evaluate"}

## Règles d'or
- Timeout global strict: 2 secondes max
- Aucune navigation Page.navigate (ne fait que test de connectivité)
- Résultat JSON structuré pour intégration pipeline
- Échec = ne pas envoyer, alerter opérateur

## Preuve d'exécution
- Date/heure : 2026-11-23T22:40:00Z
- WAL: 0x243
- IntentHash: 0xM3_SKILL_CDP_PREFLIGHT_SENTINEL_20261123

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Script principal | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-preflight-sentinel\preflight_sentinel.py` |
| Hook pre-commit | `.git/hooks/pre-push` (optionnel, appelle preflight avant push) |
| Config | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-preflight-sentinel\config.json` |

## Hash de ce skill
Horodatage: 2026-11-23T22:45:00Z | WAL: 0x243 | IntentHash: 0xM3_SKILL_CDP_PREFLIGHT_SENTINEL_20261123