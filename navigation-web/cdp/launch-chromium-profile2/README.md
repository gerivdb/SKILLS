# launch-chromium-profile2 — README d'usage

## Pré-requis

- PowerShell 7+
- Chromium installé à `C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe`
- Le dossier `C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2` existe

## Commande

```powershell
pwsh -File "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\navigation-web\cdp\launch-chromium-profile2\scripts\launch_profile2_wrapper.ps1"
```

## Vérification

Après exécution, confirmer que le port CDP répond :

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 2
```

Résultat attendu : un objet JSON contenant `Browser`, `Protocol-Version`, `User-Agent`.

## Codes de sortie

| Code | Signification |
|------|---------------|
| 0 | Succès : Chromium Profil 2 opérationnel sur le port 9222 |
| 1 | Échec : dossier introuvable, échec WMI, ou port non réponse dans les 6 s |

## Règle d'or

Aucun lancement manuel de `chrome.exe` ou `chromium.exe` sans cette compétence. WEBX (L2-PLATFORM) est le seul lanceur autorisé en alternative via `webx session start`.
