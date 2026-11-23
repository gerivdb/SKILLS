from playwright.sync_api import sync_playwright
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
context = browser.contexts[0]
page = context.new_page()
page.goto('chrome://extensions')
page.wait_for_timeout(3000)

# Cliquer sur le bouton "Charger l'extension non empaquetée" (index 3)
buttons = page.query_selector_all('button')
if len(buttons) > 3:
    btn = buttons[3]
    print(f'Clic sur le bouton: "{btn.inner_text()}"')
    btn.click()
    page.wait_for_timeout(3000)
    print('Apres clic, titre:', page.title())
    print('URL:', page.url)
    
    # Verifier si une boite de dialogue est apparue
    dialogs = page.query_selector_all('[role="dialog"], .cr-dialog, .file-picker')
    print(f'Nombre de boites de dialogue: {len(dialogs)}')
else:
    print('Bouton non trouve')

page.close()
browser.close()
p.stop()
print('TERMINE')