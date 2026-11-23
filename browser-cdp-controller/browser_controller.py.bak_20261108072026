#!/usr/bin/env python3
"""Skill: browser-cdp-controller
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

    # Ajout : get_axtree (primitive AXTree)
    async def get_axtree(page):
        """Retourne le Full AXTree via CDP. Plus robuste aux refontes CSS que DOM pur."""
        client = await page.context.new_cdp_session(page)
        try:
            tree = await client.send("Accessibility.getFullAXTree")
            return tree
        finally:
            await client.detach()

    # Ajout : capture_storage_state (primitive storage_state)
    async def capture_storage_state(context, out_path):
        """Exporte storage_state standardisé, SANS valeurs de cookies/tokens."""
        state = await context.storage_state()
        sanitized = {
            "version": 1,
            "cookies_meta": [
                {k: c[k] for k in ("name","domain","path","secure","httpOnly","expires") if k in c}
                for c in state.get("cookies", [])
            ],
            "origins_meta": [
                {"origin": o["origin"], "localStorage_keys": [x["name"] for x in o.get("localStorage", [])]}
                for o in state.get("origins", [])
            ]
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(sanitized, f, indent=2)
        return out_path

    # Ajout : launch_chromium (primitive lifecycle)
    async def launch_chromium(profile_dir, port=9222, extra_args=None):
        """Lance Chromium en mode debug CDP sur le port spécifié."""
        from pyppeteer import launch
        args = [
            "--user-data-dir", profile_dir,
            "--remote-debugging-port", str(port),
            "--password-store=basic",
            "--no-first-run",
            "--disable-gpu"
        ]
        if extra_args:
            args.extend(extra_args)
        browser = await launch(args=args, headless=False)
        page = await browser.pages()[0] if browser.pages() else None
        return browser, page

    def stop_chromium(context):
        """Arrête ownContext proprement."""
        context.close()

    async def restart_chromium(context, profile_dir, port):
        """Redémarre Chromium sur un port donné en préservant le contexte."""
        stop_chromium(context)
        _, _ = await launch_chromium(profile_dir, port)

    async def is_chromium_alive(port):
        """Vérifie si un CDP écoute sur le port donné."""
        import urllib.request
        try:
            r = urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=2)
            return r.status == 200
        except Exception:
            return False

browser_controller.get_axtree = browser_controller.BrowserController.get_axtree


browser_controller.get_axtree = browser_controller.BrowserController.get_axtree
browser_controller.get_axtree = browser_controller.BrowserController.get_axtree
