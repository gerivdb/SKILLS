# METASKILL — Chromium Profile 2 : Navigateur Attitré d'ENV2

## 1. Identité Absolue
ENV2 possède un et un seul navigateur attitré : **Chromium**, configuré avec le profil **"Profile 2"**.
- **Binaire** : `C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe`
- **Profil** : `C:\Users\GG\AppData\Local\Chromium\User Data` (sous-dossier `Profile 2`)
- **Port CDP** : `9222`

## 2. Règles d'Or (Non négociables)
1. **JAMAIS** de `playwright.chromium.launch()`. Cela crée une session vide sans cookies.
2. **TOUJOURS** de `playwright.chromium.connect_over_cdp("http://localhost:9222")`.
3. **JAMAIS** de `browser.new_context()`. On utilise le contexte existant `browser.contexts[0]`.
4. **TOUJOURS** vérifier que l'URL ne redirige pas vers `accounts.google.com` (preuve que la session est perdue).

## 3. Lancement (HITL ou Automatisé)
Le port CDP doit être ouvert. Si le navigateur est fermé, la commande exacte est :
```powershell
& "C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="C:\Users\GG\AppData\Local\Chromium\User Data" `
  --profile-directory="Profile 2" `
  --remote-allow-origins=* `
  --restore-last-session
```

## 4. Le Principe des Primitives
Une fois connecté, ENV2 a la maîtrise totale du navigateur via le protocole CDP :
- Lister, créer, fermer des onglets.
- Naviguer vers n'importe quelle URL.
- Interagir avec le DOM (cliquer, taper du texte, lire).
- Capturer des screenshots.
- Exécuter du JavaScript dans la page.

## 5. Sécurité
Les cookies de `Profile 2` sont souverains. Aucun script ne doit tenter de les extraire (App-Bound Encryption). L'interaction se fait exclusivement via Playwright sur la session déjà authentifiée.
