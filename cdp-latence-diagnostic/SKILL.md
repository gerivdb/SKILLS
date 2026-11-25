# M3 Skill — CDP Latence Diagnostic
WAL: 0x243 | F = 0.0 | H = 0.0 | Strate: ENV2 | Type: SKILL | Version: 1.0
IntentHash: 0xSKILL_CDP_LATENCE_DIAGNOSTIC_20261125

## Définition
Diagnostique la latence CDP élevée (103.77ms mesurée) sur Chromium Profil 2 (port 9222). Compte les onglets ouverts, liste les extensions actives, mesure la taille du DOM de l'onglet Gemini, et effectue des mesures de latence répétées pour identifier la cause racine.

## Problème traité
Latence CDP directe de 103.77ms — trop élevée pour un tunnel d'écriture fluide. Causes potentielles : trop d'onglets, extensions actives, DOM volumineux, charge CPU/mémoire sur la station HP Z600.

## Prérequis
- Chromium lancé avec --remote-debugging-port=9222 --remote-allow-origins=* sur ENV2 (Profil 2)
- Port 9222 en écoute sur 127.0.0.1
- Python avec modules websocket, urllib.request, psutil (optionnel)

## GESTES (séquence atomique)

### GESTE-1 — Compter les onglets ouverts
```
GET http://127.0.0.1:9222/json/list
→ Compter le nombre d'onglets de type "page"
→ Identifier les onglets Gemini vs autres
```

### GESTE-2 — Lister les extensions actives
```
GET http://127.0.0.1:9222/json/version (pour infos navigateur)
→ Vérifier les extensions via l'API extensions si disponible
```

### GESTE-3 — Mesurer la taille du DOM de l'onglet Gemini
```
CDP: Runtime.evaluate sur document.documentElement.outerHTML.length
→ Taille du HTML de l'onglet Gemini
CDP: Runtime.evaluate sur document.querySelectorAll('*').length
→ Nombre d'éléments DOM
```

### GESTE-4 — Mesurer la latence CDP (N mesures)
```
Répéter N fois (ex: 10) :
  CDP: Runtime.evaluate ("1+1")
  Mesurer le temps de réponse
→ Calculer latence moyenne, min, max, écart-type
```

### GESTE-5 — Vérifier la charge système
```
psutil : CPU %, mémoire du processus Chromium
→ Identifier si la station est saturée
```

## Paramètres d'entrée
| Paramètre | Type | Description |
|-----------|------|-------------|
| cdp_tab_id | string (optionnel) | ID de l'onglet CDP cible |
| n_measurements | integer | Nombre de mesures de latence (défaut: 10) |

## Résultat de sortie
```json
{
  "ok": true,
  "skill": "cdp-latence-diagnostic",
  "playground": "gemini",
  "tabs_count": N,
  "gemini_tabs_count": N,
  "dom_element_count": N,
  "dom_html_size_bytes": N,
  "latency_ms": {"min": N, "max": N, "avg": N, "p95": N},
  "chromium_cpu_percent": N,
  "chromium_memory_mb": N,
  "timestamp_utc": "...",
  "cdp_tab_id": "..."
}
```

## Règles d'or
- Mesures répétées pour écarter la variance
- Aucun envoi réseau direct, tout passe par CDP
- Respecter chromium-runtime-invariants (Profil 2 uniquement)

## Preuve d'exécution
- Horodatage UTC
- Nombre de mesures et statistiques de latence
- État des onglets et extensions

## Fichiers associés
| Fichier | Chemin absolu |
|---------|--------------|
| Skill definition | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-latence-diagnostic\SKILL.md` |
| Implémentation | `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cdp-latence-diagnostic\impl\cdp_latence_diagnostic.py` |

## Hash de ce skill
Horodatage: 2026-11-25T02:XX:XXZ | WAL: 0x243 | IntentHash: 0xSKILL_CDP_LATENCE_DIAGNOSTIC_20261125
