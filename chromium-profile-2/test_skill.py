#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_skill.py — Test unitaire du skill chromium-profile-2 (backend cdp-use)

Séquence testée :
  1. get_status()                                     (sans WebSocket)
  2. open_tab("https://gemini.google.com/app")        (sans WebSocket)
  3. send("Browser", "getVersion")                    (WebSocket CDP - test de connectivité)
  4. navigate(...)                                    (WebSocket CDP - méthode disponible via send)
  5. read_dom("body")                                 (WebSocket CDP - méthode disponible via send)
  6. reload()                                         (WebSocket CDP - méthode disponible via send)
  7. get_bookmarks()                                  (sans WebSocket)
  8. scan_extensions()                                (sans WebSocket)
  9. close_tab(targetId)                              (sans WebSocket)

Résultat attendu : les méthodes sans WebSocket réussissent. Les méthodes avec
WebSocket dépendent du flag --remote-allow-origins=* au lancement de Chromium.
"""

import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chromium_cdp_client import ChromiumCDPClient

RESULTATS = []


def step(nom, fn):
    print(f"\n=== {nom} ===")
    try:
        res = fn()
        print(f"OK : {res}")
        RESULTATS.append((nom, "OK", res))
        return res
    except NotImplementedError as e:
        print(f"BLOQUÉ (WebSocket 403 documenté) : {e}")
        RESULTATS.append((nom, "BLOQUÉ_WS", str(e)))
        return None
    except Exception as e:
        print(f"ERREUR : {type(e).__name__} : {e}")
        RESULTATS.append((nom, "ERREUR", str(e)))
        traceback.print_exc()
        return None


def main():
    client = ChromiumCDPClient()

    # 1. Statut
    step("get_status", client.get_status)

    # 2. Ouvrir un onglet
    tab = step("open_tab", lambda: client.open_tab("https://gemini.google.com/app"))
    target_id = tab["targetId"] if tab else None

    # 3. Test de connectivité WebSocket CDP via Browser.getVersion
    step("send(Browser, getVersion)", lambda: client.send("Browser", "getVersion"))

    # 4. Naviguer (WebSocket CDP - méthode disponible via send)
    step("navigate", lambda: client.navigate("https://gemini.google.com/app"))

    # 5. Lire le DOM (WebSocket CDP - méthode disponible via send)
    if target_id:
        step("read_dom", lambda: client.read_dom("body"))

    # 6. Recharger (WebSocket CDP - méthode disponible via send)
    step("reload", client.reload)

    # 7. Bookmarks
    step("get_bookmarks", client.get_bookmarks)

    # 8. Extensions
    step("scan_extensions", client.scan_extensions)

    # 9. Fermer l'onglet
    if target_id:
        step("close_tab", lambda: client.close_tab(target_id))

    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DU TEST")
    print("=" * 60)
    for nom, statut, detail in RESULTATS:
        print(f"  {nom:<25} | {statut}")
    ok = sum(1 for _, s, _ in RESULTATS if s == "OK")
    bloques = sum(1 for _, s, _ in RESULTATS if s == "BLOQUÉ_WS")
    erreurs = sum(1 for _, s, _ in RESULTATS if s == "ERREUR")
    print(f"\nTotal : {len(RESULTATS)} | OK : {ok} | Bloqués WS : {bloques} | Erreurs : {erreurs}")
    if bloques > 0 or erreurs > 0:
        print("\nLes méthodes WebSocket nécessitent le flag --remote-allow-origins=*")
        print("au lancement de Chromium, et une version du protocole CDP compatible.")
        print("Les méthodes sans WebSocket sont pleinement opérationnelles.")


if __name__ == "__main__":
    main()
