# Skill : chrome-vs-chromium-target-check

## Déclencheurs

- Avant toute commande qui lance Chrome ou Chromium (`chrome.exe`, `chromium.exe`)
- Avant toute opération qui utilise `--user-data-dir`, `--profile-directory`, ou `--remote-debugging-port`
- Avant toute opération qui interagit avec un navigateur via CDP (Chrome DevTools Protocol)
- Avant toute opération qui dépend d'un profil utilisateur Chrome/Chromium

## Règles (numérotées, impératives)

1. Vérifier le chemin exact de l'exécutable : `chrome.exe` (Google Chrome) et `chrome.exe` (Chromium/ungoogled-chromium) sont des binaires différents.
2. Vérifier `--user-data-dir` : ne jamais supposer que c'est `C:\Users\GG\AppData\Local\Chromium\User Data`. Vérifier le chemin exact.
3. Vérifier `--profile-directory` : ne pas supposer "Default". Le profil peut être "Profile 2", "Default", ou tout autre nom.
4. Vérifier `--remote-debugging-port` : spécifier explicitement le port (ex: 9222). Ne pas supposer qu'il est déjà occupé par une autre instance.
5. Avant toute opération de débugging CDP, vérifier que le port est accessible et que le bon profil est chargé.

## Anti-patterns (interdits documentés)

- Utiliser `--user-data-dir` sans `--profile-directory` (charge le profil "Default" par défaut, qui peut être vide ou vide de cookies).
- Utiliser `--profile-directory="Profile 2"` sans `--user-data-dir` (Chrome 136+ ignore le debugging si `--user-data-dir` est absent).
- Utiliser `--remote-debugging-address=0.0.0.0` (expose le débogage à tout le LAN).
- Utiliser `taskkill /IM chrome.exe` pour "nettoyer" : tue toutes les instances, y compris celles d'autres shards.
- Lancer Chrome avec une URL en argument si une instance est déjà lancée (le nouveau processus passe l'URL à l'existant et se ferme).

## Preuve de vie

- `Test-Path` sur le chemin exact de l'exécutable Chrome/Chromium.
- `Test-Path` sur le répertoire `--user-data-dir`.
- `Test-Path` sur `C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2\Cookies` (preuve que le profil contient des données).
- `Get-Process chrome` ou `Get-Process chromium` (vérifier que l'instance est lancée).
- `Get-Content` sur `C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2\Default\Cookies` (si applicable) ou sur le fichier de cookies du profil cible.

## Configuration

Aucun paramètre configurable. Les chemins et dépendances dépendent du contexte d'exécution.
