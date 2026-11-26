#!/usr/bin/env python3
"""Script: verify_extensions_installed.py
Rôle : Vérifier que les 3 extensions Comet sont actives via CDP management.getAll.
Contrainte : Attach-only CDP sur port 9222.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

CDP_URL = "http://localhost:9222"

EXTENSION_IDS = [
    "mcjlamohcooanphmebaiigheeeoplihb",      # Comet
    "mjdcklhepheaaemphcopihnmjlmjpcnh",      # Comet Web Resources
    "npclhjbddhklpbnacpjloidibaggcgon",      # comet-agent
]


def cdp_get(endpoint: str, timeout: int = 10):
    url = f"{CDP_URL}{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"ERREUR_CDP_GET {url}: {e}")
        return None


def main():
    print("[verify_extensions_installed] Vérification des extensions Comet via CDP...")

    result = cdp_get("/json/Extension.getAll")
    if result is None:
        print("ERREUR: Impossible de contacter le CDP sur le port 9222")
        sys.exit(1)

    if not isinstance(result, list):
        print(f"ERREUR: Réponse CDP inattendue: {result}")
        sys.exit(1)

    installed_ids = {ext.get("id") for ext in result if isinstance(ext, dict)}
    active_ids = {
        ext.get("id") for ext in result
        if isinstance(ext, dict) and ext.get("enabled") is True
    }

    all_installed = True
    for ext_id in EXTENSION_IDS:
        if ext_id in installed_ids:
            status = "ACTIVE" if ext_id in active_ids else "INACTIVE"
            print(f"  OK: {ext_id} — {status}")
            if ext_id not in active_ids:
                all_installed = False
        else:
            print(f"  MANQUANT: {ext_id} — non installé")
            all_installed = False

    if all_installed:
        print("extensions_activees=true")
        print("Toutes les extensions Comet sont installées et actives")
        sys.exit(0)
    else:
        print("extensions_activees=false")
        print("Certaines extensions Comet sont manquantes ou inactives")
        sys.exit(1)


if __name__ == "__main__":
    main()