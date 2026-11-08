# METASKILL — Chromium CDP & Session Persistante (ENV2)

## 1. Le Problème
Google Chrome et Chromium (>= v127) chiffrent les cookies (App-Bound Encryption). 
Les extraire via un script externe (SQLite + DPAPI) est devenu extrêmement fragile et souvent impossible.
L'API `gpsoauth` nécessite un `oauth_token` qui n'est PAS présent dans les cookies web standards.

## 2. La Solution (Validée)
L'extraction des données se fait **exclusivement via le DOM** de la page déjà ouverte.
Pour cela, on utilise le **Chrome DevTools Protocol (CDP)**.

### Règle d'or de l'automatisation
1. **L'humain lance le navigateur** avec son profil réel (`Profile 2`) et le port CDP.
2. **Le script se connecte** au port. Il ne lance JAMAIS le navigateur.

### Commandes de lancement (HITL)
```powershell
& "C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="C:\Users\GG\AppData\Local\Chromium\User Data" `
  --profile-directory="Profile 2" `
  --remote-allow-origins=*
```

### Code Playwright (Skill)
**INCORRECT (crée un profil vide)** :
```python
browser = p.chromium.launch(headless=False) # ❌
```

**CORRECT (utilise le profil existant)** :
```python
browser = p.chromium.connect_over_cdp("http://localhost:9222") # ✅
```

## 3. Pourquoi ça marche
On n'essaie pas de "voler" les cookies. Playwright pilote l'onglet en tant qu'utilisateur légitime. 
Les cookies sont déjà gérés par Chromium. Le DOM est accessible nativement.
