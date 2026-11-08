from browser_controller import BrowserController


def test_deepseek():
    with BrowserController() as bc:
        # 1. Ouvrir l'onglet DeepSeek
        print("Ouverture de DeepSeek...")
        page = bc.open_tab("https://chat.deepseek.com")

        # 2. Vérifier si on est authentifié (pas de redirection vers /signin)
        if "signin" in page.url:
            print("AUTH_REQUISE: Veuillez vous connecter manuellement dans cet onglet.")
            return

        print(f"Onglet prêt: {page.title()}")

        # 3. Test d'écriture (inspection du sélecteur du chat DeepSeek)
        # page.locator('textarea').fill("Test prompt")
        # page.locator('button[type="submit"]').click()
        print("Prêt à interagir avec le DOM DeepSeek.")


if __name__ == "__main__":
    test_deepseek()
