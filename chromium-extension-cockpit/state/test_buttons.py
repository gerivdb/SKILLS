from playwright.sync_api import sync_playwright
p = sync_playwright().start()
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
context = browser.contexts[0]
page = context.new_page()
page.goto('chrome://extensions')
page.wait_for_timeout(3000)

# Chercher tous les boutons et toggles
buttons = page.query_selector_all('button, cr-toggle-button, [role="button"], [role="switch"]')
print(f'Nombre de boutons/toggles trouves: {len(buttons)}')
for i, btn in enumerate(buttons):
    try:
        text = btn.inner_text()[:50] if btn.inner_text() else ''
        aria = btn.get_attribute('aria-label') or ''
        name = btn.get_attribute('name') or ''
        print(f'  [{i}] text="{text}" aria-label="{aria}" name="{name}"')
    except Exception as ex:
        print(f'  [{i}] (erreur: {ex})')

page.close()
browser.close()
p.stop()
print('TERMINE')