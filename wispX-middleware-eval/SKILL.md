# M3 Skill — WISPX Middleware Évaluation
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_WISPX_MIDDLEWARE_EVAL_20261125

## Définition
Évalue le rôle du middleware WISPX (port 9333) dans le pipeline d'écriture CDP vers Chromium/Profil 2. Détermine si WISPX est un point de passage obligatoire, un proxy, ou une couche optionnelle dans le tunnel d'écriture.

## Contexte
- CDP : port 9222 (accès direct au navigateur Chromium Profil 2)
- WISPX : port 9333 (middleware mentionné comme intermédiaire potentiel)
- Objectif : établir un "véritable tunnel d'écriture" optimisé

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Port 9333 (WISPX) à vérifier
- Python avec modules urllib.request, socket

## GESTES (séquence atomique)

### GESTE-1 — Vérifier le port CDP 9222
```
GET http://127.0.0.1:9222/json/version
→ Confirmer que CDP répond
```

### GESTE-2 — Vérifier le port WISPX 9333
```
Test de connexion TCP sur 127.0.0.1:9333
→ Déterminer si WISPX est actif
GET http://127.0.0.1:9333/health (si endpoint existe)
→ Vérifier si WISPX expose une API de health
```

### GESTE-3 — Comparer latence CDP direct vs via WISPX
```
Mesurer latence d'une commande Runtime.evaluate via CDP direct (port 9222)
Mesurer latence d'une commande équivalente via WISPX (port 9333, si disponible)
→ Comparer les deux latences
```

### GESTE-4 — Déterminer le rôle de WISPX
```
Si WISPX actif et expose une API de relay CDP → WISPX est un proxy/intermédiaire
Si WISPX inactif → CDP direct est le seul chemin, WISPX n'est pas dans le tunnel d'écriture
Si WISPX actif mais pas d'API de relay → WISPX est un middleware indépendant, pas dans le tunnel d'écriture Chromium
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| wispX_port | integer | Port du middleware WISPX (défaut: 9333) |
| cdp_port | integer | Port CDP Chromium (défaut: 9222) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "wispX-middleware-eval",
  "cdp_port": 9222,
  "wispX_port": 9333,
  "cdp_active": true,
  "wispX_active": false,
  "wispX_has_health_endpoint": false,
  "wispX_is_cdp_proxy": false,
  "latency_cdp_direct_ms": N,
  "latency_wispX_ms": null,
  "recommendation": "CDP direct uniquement / WISPX intermédiaire recommandé / WISPX à contourner",
  "timestamp_utc": "..."
}
```

## Règles d'or
- Jamais de requête HTTP directe hors CDP/WISPX (règle BDCP)
- Évaluation factuelle, pas d'hypothèse sur le rôle de WISPX
- Mesure de latence réelle sur ENV2

## Preuve d'exécution
- Horodatage UTC
- État actif/inactif de chaque port
- Latences mesurées
- Recommandation d'architecture

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wispX-middleware-eval\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wispX-middleware-eval\impl\wispX_middleware_eval.py` |

## Hash de ce skill
Horodatage: 2026-11-25T02:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_WISPX_MIDDLEWARE_EVAL_20261125
