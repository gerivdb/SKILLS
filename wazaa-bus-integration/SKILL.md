# M3 Skill — WAZAA Bus Integration
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: L4-TOOLS | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_WAZAA_BUS_INTEGRATION_20261125

## Définition
Définit le protocole de message WAZAA pour le tunnel d'écriture ENV2 ↔ ENV3. WAZAA est le système bus du métacluster (super-projet référençant tous les repos comme sous-modules). Il doit remplacer le tunnel CDP persistant point-à-point par un bus de messages structuré, avec WISPX comme middleware de pont unique.

## Problème traité
Actuellement : tunnel CDP persistant point-à-point (port 9222, Profil 2). Limites : point unique de défaillance, pas de multiplexing, pas de routage intermédiaire, pas de file d'attente en cas de coupure.
WAZAA offre : bus de messages, sous-modules (dont WISPX comme middleware de pont), orchestrateur de continuité conversationnelle.

## Constat d'anomalie (à corriger)
WISPX est référencé à deux endroits dans le super-projet WAZAA :
- `L1-INFRA/WISPX/` (middleware de pont, correct)
- `L2-PLATFORM/WISPX/` (doublon, à supprimer)
Recommandation : garder uniquement `L1-INFRA/WISPX/` comme middleware de pont unique.

## Prérequis
- Repo WAZAA cloné localement : `D:\DO\WEB\TOOLS\WAZAA` (chemin SOT connu_repositories.yaml)
- Port CDP 9222 actif (Profil 2) pour validation croisée
- Port WISPX 9333 actif (middleware de pont)
- Python avec modules subprocess, json, hashlib, urllib.request, sqlite3, pathlib

## GESTES (séquence atomique)

### GESTE-1 — Audit de l'état du bus WAZAA
```
Vérifier que D:\DO\WEB\TOOLS\WAZAA existe et est un repo git
Lister les sous-modules WISPX référencés (L1-INFRA/WISPX et L2-PLATFORM/WISPX)
→ Détecter le doublon WISPX
→ Recommander la suppression de L2-PLATFORM/WISPX
```

### GESTE-2 — Définition du format de message WAZAA
```
Format JSON enveloppé pour le tunnel ENV2 ↔ ENV3 :
{
  "envelope": {
    "bus": "WAZAA",
    "version": "1.0",
    "timestamp_utc": "...",
    "wal_seal": "WAL-0x243",
    "message_id": "..."
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

### GESTE-3 — Intégration du tunnel CDP persistant comme premier hop
```
Le tunnel CDP persistant (skill cdp-tunnel-persistant) reste le premier hop (port 9222).
WAZAA devient le bus de routage au-dessus : messages WAZAA encapsulés dans le tunnel CDP.
WISPX (port 9333) devient le middleware de relais authentifié (après résolution du 401).
```

### GESTE-4 — Validation du protocole sur le bus WAZAA local
```
Lire l'état des sous-modules WAZAA (git submodule status)
Vérifier que WISPX L1-INFRA/WISPX est présent et actif
Vérifier que WISPX L2-PLATFORM/WISPX est le doublon à supprimer
Produire le rapport de validation JSON
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| wazaa_path | string | Chemin absolu vers le repo WAZAA (défaut: D:\DO\WEB\TOOLS\WAZAA) |
| fix_duplicate_wispX | boolean | Si true, supprimer le sous-module L2-PLATFORM/WISPX (défaut: false, audit uniquement) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "wazaa-bus-integration",
  "playground": "gemini",
  "wazaa_path": "D:\\DO\\WEB\\TOOLS\\WAZAA",
  "wispX_locations": ["L1-INFRA/WISPX", "L2-PLATFORM/WISPX"],
  "wispX_duplicate_detected": true,
  "recommendation": "Supprimer L2-PLATFORM/WISPX, garder L1-INFRA/WISPX comme middleware de pont unique",
  "message_format": "WAZAA JSON enveloppé (envelope + payload + proof)",
  "first_hop": "CDP tunnel persistant (port 9222, Profil 2)",
  "relay_middleware": "WISPX (port 9333, L1-INFRA/WISPX)",
  "timestamp_utc": "...",
  "sha256_proof": "...",
  "exit_code": 0
}
```

## Règles d'or
- Jamais de modification de WAZAA sans HITL explicite (ce skill est en mode audit uniquement par défaut)
- WISPX doit être présent une seule fois : L1-INFRA/WISPX
- Le bus WAZAA encapsule le tunnel CDP, ne le remplace pas entièrement
- Preuve brute obligatoire : hash SHA-256 + timestamp UTC + exit_code + wal_seal

## Preuve d'exécution
- Horodatage UTC
- État des sous-modules WISPX détecté
- Hash SHA-256 du rapport
- exit_code = 0

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wazaa-bus-integration\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wazaa-bus-integration\impl\wazaa_bus_integration.py` |

## Hash de ce skill
Horodatage: 2026-11-25T03:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_WAZAA_BUS_INTEGRATION_20261125
