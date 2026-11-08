#!/usr/bin/env python3
"""
Skill: browser-cdp-controller
Rôle: Primitives de pilotage du navigateur attitré (Chromium Profile 2) via CDP.
Contrainte: Ne JAMAIS lancer le navigateur via Playwright (launch), TOUJOURS se connecter (connect_over_cdp).
"""
import sys
from playwright.sync_api import sync_playwright


class BrowserController:
    def __init__(self, port=9222):
        self.cdp_url = f"http://localhost:{port}"
        self.playwright = None
        self.browser = None
        self.context = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.connect_over_cdp(self.cdp_url)
        except Exception as e:
            print(f"ERREUR_CDP: Port {self.cdp_url} injoignable. Lancez Chromium avec --remote-debugging-port=9222.")
            sys.exit(1)
        if not self.browser.contexts:
            print("ERREUR_CONTEXTE: Aucun contexte trouvé.")
            sys.exit(1)
        self.context = self.browser.contexts[0]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # On ne ferme PAS le navigateur, on ferme juste la connexion Playwright
        self.playwright.stop()

    def list_tabs(self):
        """Retourne la liste des onglets ouverts."""
        return [{"index": i, "url": pg.url, "title": pg.title()} for i, pg in enumerate(self.context.pages)]

    def open_tab(self, url, wait_for_load=True):
        """Ouvre un nouvel onglet."""
        page = self.context.new_page()
        if wait_for_load:
            page.goto(url, wait_until="networkidle")
        else:
            page.goto(url)
        return page

    def close_tab(self, index):
        """Ferme un onglet par son index."""
        if index < len(self.context.pages):
            self.context.pages[index].close()

    def navigate(self, page, url):
        """Navigue un onglet existant."""
        page.goto(url, wait_until="networkidle")

    def read_text(self, page, selector):
        """Lit le texte d'un élément."""
        return page.locator(selector).inner_text()

    def type_text(self, page, selector, text):
        """Remplit un champ de texte."""
        page.locator(selector).fill(text)

    def click(self, page, selector):
        """Clique sur un élément."""
        page.locator(selector).click()


if __name__ == "__main__":
    # Test rapide
    with BrowserController() as bc:
        print("Onglets ouverts :")
        for tab in bc.list_tabs():
            print(f"[{tab['index']}] {tab['title']} - {tab['url']}")
