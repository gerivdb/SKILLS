#!/usr/bin/env python3
"""
Skill: browser-dom-extractor
Rôle: Se connecter à une instance Chromium existante via CDP et extraire le DOM.
Contrainte: Ne JAMAIS lancer le navigateur via Playwright (launch), TOUJOURS se connecter (connect_over_cdp).
"""
import sys
import json
from playwright.sync_api import sync_playwright

def extract_from_cdp(port: int, url: str, css_selector: str):
    cdp_url = f"http://localhost:{port}"
    with sync_playwright() as p:
        try:
            # On se connecte à la session existante (Profile 2)
            browser = p.chromium.connect_over_cdp(cdp_url)
        except Exception as e:
            print(f"ERREUR_CDP: Impossible de se connecter au port {port}. Chromium est-il lancé avec --remote-debugging-port={port} ?")
            sys.exit(1)
            
        if not browser.contexts:
            print("ERREUR_CONTEXTE: Aucun contexte trouvé.")
            sys.exit(1)
            
        context = browser.contexts[0]
        
        # Chercher un onglet existant ou en créer un
        page = next((pg for pg in context.pages if url in pg.url), None)
        if not page:
            page = context.new_page()
            page.goto(url, wait_until="networkidle")
        
        # Vérifier si on est redirigé vers la page de login
        if "accounts.google.com" in page.url:
            print("ERREUR_AUTH: Redirigé vers la page de connexion. Le profil n'est pas connecté.")
            sys.exit(2)
            
        # Extraction
        elements = page.evaluate(f"""
            () => {{
                const els = document.querySelectorAll('{css_selector}');
                return Array.from(els).map(e => e.innerText);
            }}
        """)
        
        print(json.dumps({"url": page.url, "count": len(elements), "data": elements}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    # Cible par défaut : Keep, notes-container
    extract_from_cdp(9222, "https://keep.google.com", ".notes-container")
