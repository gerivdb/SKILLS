# M3 Skill — WAZAA Bus Relay
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: L4-TOOLS | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_WAZAA_BUS_RELAY_20261125

## Définition
Implémente le relais du bus WAZAA sur le tunnel CDP persistant (port 9222, Profil 2). Encapsule les messages au format WAZAA JSON enveloppé et les envoie à ENV3 (Gemini) via CDP. Lit la réponse et vérifie la preuve d'intégrité (hash SHA-256, timestamp UTC, wal_seal).

## Architecture d'intégration
ENV2 → CDP tunnel persistant (port 9222, Profil 2) → WAZAA bus enveloppé → Gemini ENV3

WAZAA ne remplace pas le tunnel CDP : il l'encapsule. Le tunnel reste le premier hop physique. WAZAA ajoute le routage, le format de message structuré et la preuve d'intégrité.

## Prérequis
- Compétence cdp-tunnel-persistant déjà validée (1 connexion WebSocket, 1.864ms latence)
- Compétence cdp-chat-gemini-read-v2 déjà validée (sélecteur div.markdown-main-panel.md-content)
- Chromium lancé avec --remote-debugging-port=9222 sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Onglet Gemini ouvert sur https://gemini.google.com/app

## GESTES (séquence atomique)

### GESTE-1 — Construire le message WAZAA
```
Créer un objet JSON enveloppé :
{
  "envelope": {
    "bus": "WAZAA",
    "version": "1.0",
    "timestamp_utc": "...",
    "wal_seal": "WAL-0x243",
    "message_id": "<hash SHA-256>"
  },
  "payload": {
    "action": "...",
    "target": "...",
    "source_env": "ENV2",
    "target_env": "ENV3",
    "skill": "...",
    "intent_hash": "...",
    "exit_code": 0,
    "sha256_before": "...",
    "sha256_after": "...",
    "state_before": "...",
    "state_after": "..."
  },
  "proof": {
    "hash_sha256": "...",
    "verified": true
  }
}
```

### GESTE-2 — Ouvrir le tunnel CDP persistant
```
WebSocket connect: ws://127.0.0.1:9222/devtools/page/<target_id>
CDP: Runtime.enable (une seule fois)
CDP: Page.enable (une seule fois)
```

### GESTE-3 — Injecter le message WAZAA dans Gemini
```
CDP: Runtime.evaluate
expression: inject le JSON WAZAA dans la zone de saisie (div.ql-editor.textarea)
dispatchEvent('input')
```

### GESTE-4 — Cliquer sur Envoyer
```
CDP: Runtime.evaluate
expression: clic sur button[aria-label="Envoyer un message"]
```

### GESTE-5 — Lire la réponse ENV3
```
Polling avec détection de stabilité sur div.markdown-main-panel.md-content
→ Capturer le texte de la réponse
→ Vérifier le hash SHA-256 de la réponse
```

### GESTE-6 — Fermer le tunnel
```
WebSocket close
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| action | string | Action du message WAZAA |
| target | string | Cible du message |
| source_env | string | Environnement source (défaut: ENV2) |
| target_env | string | Environnement cible (défaut: ENV3) |
| skill | string | Nom du skill émetteur |
| intent_hash | string | IntentHash de l'action |
| state_before | string | État avant l'action |
| state_after | string | État après l'action |
| exit_code | integer | Code de retour (défaut: 0) |
| sha256_before | string | Hash avant (défaut: "") |
| sha256_after | string | Hash après (défaut: "") |
| cdp_tab_id | string | ID de l'onglet CDP (optionnel) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "wazaa-bus-relay",
  "playground": "gemini",
  "waZAA_message_id": "...",
  "waZAA_message_sha256": "...",
  "inject_result": "...",
  "send_result": "clicked",
  "connections_used": 1,
  "connections_saved": 2,
  "response": "<texte réponse ENV3>",
  "response_length": N,
  "response_sha256": "...",
  "latency_ms": N,
  "timestamp_utc": "...",
  "cdp_tab_id": "..."
}
```

## Règles d'or
- Jamais de requête HTTP directe, tout passe par CDP (règle BDCP)
- Une seule connexion WebSocket par cycle d'écriture (règle cdp-tunnel-persistant)
- Preuve brute obligatoire : hash SHA-256 + timestamp UTC + exit_code + wal_seal
- Sélecteur DOM validé : div.markdown-main-panel.md-content (règle DOM Empiricism)
- WISPX reste en arrière-plan (port 9333, authentification requise)

## Preuve d'exécution
- Horodatage UTC
- Hash SHA-256 du message WAZAA envoyé
- Hash SHA-256 de la réponse ENV3 reçue
- exit_code = 0
- wal_seal = WAL-0x243

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wazaa-bus-relay\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wazaa-bus-relay\impl\wazaa_bus_relay.py` |

## Hash de ce skill
Horodatage: 2026-11-25T03:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_WAZAA_BUS_RELAY_20261125
