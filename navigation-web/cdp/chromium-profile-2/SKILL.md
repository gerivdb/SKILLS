---
name: chromium-profile-2
description: "Pilote l'instance Chromium déjà ouverte en profil 2 (port 9222) via le Chrome DevTools Protocol (CDP) : ouvrir un onglet, naviguer, évaluer du JS, cliquer physiquement, lire bookmarks/historique, scanner les extensions."
version: 1.0.0
status: active
intent_hash: 0xSKILL_CHROMIUM_PROFILE_2_20261126
stratum: L4-TOOLS
source_repo: gerivdb/SKILLS
source_path: navigation-web/cdp/chromium-profile-2/SKILL.md
triggers:
  - "profil-2"
  - "cdp-9222"
  - "chrome-devtools"
  - "ouvre-onglet"
  - "navigue"
  - "lit-dom"
anti_triggers:
  - "chrome-exe-manuel"
  - "sans-cdp"
  - "profil-vide"
---

# Skill : chromium-profile-2 — Pilotage CDP de Chromium (profil 2)

## Objectif
Piloter l'instance Chromium déjà ouverte en profil 2 (port 9222) via le Chrome DevTools Protocol (CDP) : ouvrir un onglet, naviguer, évaluer du JS, cliquer physiquement, lire bookmarks/historique, scanner les extensions.

## Localisation
`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2/`

## Fichiers du skill
- `chromium_cdp_client.py` — client CDP basé sur `cdp-use` (57 domaines générés automatiquement).
- `SKILL.md` — ce document.
- `test_skill.py` — test unitaire de validation.

## Prérequis
- Chromium lancé avec les flags :
  `C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe --user-data-dir="C:\Users\GG\AppData\Local\Chromium\User Data" --profile-directory="Profile 2" --remote-debugging-port=9222 --remote-allow-origins=*`
- Le port 9222 doit répondre (`http://localhost:9222/json/version`).
- Python 3 avec `cdp-use` installé (`pip install cdp-use`).

## Règles de bonne pratique
- Ne JAMAIS tuer ou redémarrer le Chromium déjà ouvert (stop_browser désactivé).
- Ne JAMAIS ouvrir une nouvelle fenêtre — toujours un nouvel onglet via `open_tab`.
- Le WebSocket CDP est bloqué (403) si `--remote-allow-origins=*` est absent du lancement Chromium.
- Les méthodes de données (get_bookmarks, get_history, scan_extensions) fonctionnent sans WebSocket.

## Backend CDP — 57 domaines générés automatiquement
Le client utilise `cdp-use` (v1.4.5) qui génère à partir de la spécification officielle tous les domaines CDP :

```
accessibility, animation, audits, autofill, backgroundservice, bluetoothemulation,
browser, browseruse, cachestorage, cast, console, css, debugger, deviceaccess,
deviceorientation, dom, domdebugger, domsnapshot, domstorage, emulation,
eventbreakpoints, extensions, fedcm, fetch, filesystem, headlessexperimental,
heapprofiler, indexeddb, input, inspector, io, layertree, library, log, media,
memory, network, overlay, page, performance, performancetimeline, preload, profiler,
pwa, registration_library, registry, runtime, schema, security, serviceworker,
storage, systeminfo, target, tethering, tracing, webaudio, webauthn
```

## API — 20 méthodes exposées

### Cycle de vie
| Méthode | Rôle | WebSocket requis |
|---------|------|------------------|
| `start_browser()` | Lance Chromium (profil 2, port 9222, allow-origins) | Non |
| `stop_browser()` | Désactivé (sécurité) | Non |
| `get_status()` | Nombre d'onglets + statut WS CDP | Non |

### Onglets
| Méthode | Rôle | WebSocket requis |
|---------|------|------------------|
| `open_tab(url="about:blank")` | Ouvre un nouvel onglet via PUT /json/new | Non |
| `close_tab(target_id)` | Ferme un onglet spécifique | Non |
| `list_tabs()` | Liste tous les onglets (id, title, url, type) | Non |
| `switch_tab(target_id)` | Active un onglet (Target.activateTarget) | Oui |

### Navigation
| Méthode | Rôle | WebSocket requis |
|---------|------|------------------|
| `navigate(url)` | Va sur une URL (Page.navigate) | Oui |
| `go_back()` | Reculer (Page.goBack) | Oui |
| `go_forward()` | Avancer (Page.goForward) | Oui |
| `reload()` | Rafraîchir (Page.reload) | Oui |
| `stop_loading()` | Arrêter chargement (Page.stopLoading) | Oui |

### Interaction DOM & JS
| Méthode | Rôle | WebSocket requis |
|---------|------|------------------|
| `read_dom(selector)` | Lire textContent (Runtime.evaluate) | Oui |
| `click(selector)` | Clic physique (Input.dispatchMouseEvent) | Oui |
| `type(selector, text)` | Écrire dans un champ (Input.insertText) | Oui |
| `evaluate_js(script)` | Exécuter JS arbitraire (Runtime.evaluate) | Oui |
| `screenshot()` | Capture d'écran (Page.captureScreenshot) | Oui |

### Données (profil 2, sans WebSocket)
| Méthode | Rôle | WebSocket requis |
|---------|------|------------------|
| `get_bookmarks()` | Lit le fichier Bookmarks (JSON) | Non |
| `get_history()` | Lit l'historique SQLite (History) | Non |
| `scan_extensions()` | Scanne Extensions/ et liste les ID | Non |

## Méthode générique — send (50+ domaines CDP)
Le client expose une méthode générique pour appeler **n'importe quelle commande CDP** :

```python
await client.send("Page", "navigate", {"url": "https://example.com"})
await client.send("DOM", "getDocument", {"depth": 0})
await client.send("Network", "setCacheDisabled", {"cacheDisabled": True})
await client.send("Runtime", "evaluate", {"expression": "1+1", "returnByValue": True})
await client.send("Input", "dispatchMouseEvent", {
    "type": "mousePressed", "x": 100, "y": 200, "button": "left", "clickCount": 1
})
```

Utilisation asynchrone :
```python
from chromium_cdp_client import ChromiumCDPClient

client = ChromiumCDPClient()
result = asyncio.run(client.send("Browser", "getVersion"))
print(result)
```

## Utilisation rapide (méthodes de haut niveau)

```python
import sys, asyncio
sys.path.insert(0, r'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2')
from chromium_cdp_client import ChromiumCDPClient

client = ChromiumCDPClient()
print(client.get_status())              # onglets + statut WS
tab = client.open_tab("https://gemini.google.com/app")
print("Onglet :", tab["targetId"])
tabs = client.list_tabs()
print("Cibles :", len(tabs))
bms = client.get_bookmarks()
print("Bookmarks :", bms["count"])
exts = client.scan_extensions()
print("Extensions :", exts["count"])
client.close_tab(tab["targetId"])
```

## Test unitaire
Exécuter `test_skill.py` depuis le dossier du skill. Il ouvre un onglet, navigue vers gemini.google.com/app, lit le DOM, recharge, liste bookmarks et extensions, ferme l'onglet.

**Note :** Les étapes nécessitant le WebSocket CDP (navigate, read_dom, reload, click, type, evaluate_js, screenshot, switch_tab) échoueront avec une erreur claire si `--remote-allow-origins=*` n'est pas passé au lancement de Chromium.
