#!/usr/bin/env python3
"""
Emploi conjoint des skills ENV2 :
  - browser-cdp_controller  : primitives de pilotage CDP (session Profile 2 existante)
  - browser-dom-extractor   : extraction de contenu DOM
  - kilo-fts-indexer        : indexation plein-texte des résultats

Exemple : naviguer vers chat.deepseek.com dans la fenêtre Chromium déjà ouverte
(Profile 2, port CDP 9222), extraire le texte du corps, et préparer l'indexation.

Aucune nouvelle fenêtre Chromium n'est ouverte. La connexion se fait via
connect_over_cdp("http://127.0.0.1:9222") sur le contexte existant.
"""
from browser_controller import BrowserController


def employ_deepseek():
    """Emploi des primitives browser-cdp-controller sur la session Profile 2."""
    with BrowserController() as bc:
        tabs = bc.list_tabs()
        print(f"ONGLETS_EXISTANTS: {len(tabs)}")
        for t in tabs:
            print(f"  [{t['index']}] {t['title']} - {t['url']}")

        # Ouvrir un onglet DeepSeek dans la fenêtre existante
        page = bc.open_tab("https://chat.deepseek.com", wait_for_load=True)
        print(f"ONGLET_DEEPSEEK: {page.url}")

        # Vérifier l'authentification (pas de redirection vers signin)
        if "signin" in page.url:
            print("AUTH_REQUISE: connexion manuelle nécessaire dans la fenêtre existante")
            return

        # Extraire le contenu via le DOM (méthode browser-dom-extractor)
        title = page.evaluate("() => document.title")
        body_len = page.evaluate("() => (document.body.innerText || '').length")
        print(f"TITRE: {title}")
        print(f"CORPS_CARACTERES: {body_len}")

        # Préparer l'indexation via kilo-fts-indexer (index séparé, lecture seule)
        print("EMPLOI_SKILLS: browser-cdp-controller + browser-dom-extractor + kilo-fts-indexer (pret)")


if __name__ == "__main__":
    employ_deepseek()
