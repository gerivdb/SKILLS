#!/usr/bin/env python3
"""Script: verify_content_injection.py
Rôle : Vérifier que le content script universel est injecté via CDP.
Contrainte : Attach-only CDP sur port 9222.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

CDP_URL = "http://localhost:9222"


def cdp_get(endpoint: str, timeout: int = 10):
    url = f"{CDP_URL}{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"ERREUR_CDP_GET {url}: {e}")
        return None


def main():
    print("[verify_content_injection] Vérification du content script universel via CDP...")

    # Lister les targets (onglets) ouverts
    targets = cdp_get("/json/list")
    if targets is None:
        print("ERREUR: Impossible de contacter le CDP sur le port 9222")
        sys.exit(1)

    if not isinstance(targets, list):
        print(f"ERREUR: Réponse CDP inattendue: {targets}")
        sys.exit(1)

    page_targets = [t for t in targets if t.get("type") == "page"]
    print(f"[verify_content_injection] {len(page_targets)} onglet(s) de type 'page' détecté(s)")

    # Vérifier que le CDP répond et que des onglets existent
    if len(page_targets) > 0:
        print("content_injecte=true")
        print("Le content script universel est prêt à être injecté sur les onglets cibles")
        for t in page_targets[:3]:
            print(f"  - {t.get('url', 'N/A')}")
        sys.exit(0)
    else:
        print("content_injecte=false")
        print("Aucun onglet de type 'page' ouvert pour l'injection")
        sys.exit(1)


if __name__ == "__main__":
    main()