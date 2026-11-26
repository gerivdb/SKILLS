---
type: SKILL
name: launch-chromium-profile2
version: 1.0.0
status: active
intent_hash: 0xSKILL_LAUNCH_CHROMIUM_PROFILE2_20261126
stratum: L4-TOOLS
source_repo: gerivdb/SKILLS
source_path: navigation-web/cdp/launch-chromium-profile2/SKILL.md
path: navigation-web/cdp/launch-chromium-profile2
triggers:
  - "lance-chromium"
  - "ouvre-profil-2"
  - "cdp-9222"
  - "navigation-web"
anti_triggers:
  - "chrome-exe-manuel"
  - "sans-cdp"
  - "profil-vide"
description: "Lance Chromium en Profil 2 avec le port CDP 9222 ouvert, de manière déterministe et détachée (WMI). Vérifie que http://127.0.0.1:9222/json/version répond avant de retourner succès. Interdit tout lancement manuel de chrome.exe sans cette compétence."
---

# Skill : launch-chromium-profile2

## Objectif

Lancer Chromium (Ungoogled-Chromium ou Chromium) en **Profil 2** avec le **port CDP 9222** ouvert, de manière déterministe et détachée du Job Object Windows. Cette compétence est **obligatoire** avant toute opération de navigation web, consultation de CDP, ou interaction avec Chromium depuis KiloCode ou tout agent de l'écosystème gerivdb.

## Pré-requis

- Chromium installé à `C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe`
- Le dossier `C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2` existe
- PowerShell 7+ disponible

## Implémentation

Le script `scripts/launch_profile2_wrapper.ps1` appelle le script canonique `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\navigation-web\cdp\chromium-extension-cockpit\scripts\launch_profile2.ps1` qui :

1. Vérifie si le port 9222 répond déjà → si oui, retourne succès immédiatement
2. Purge les verrous LOCK orphelins du Profil 2
3. Répare `exit_type` dans `Preferences` si nécessaire
4. Lance Chromium détaché via WMI (`Win32_Process.Create`) avec les flags :
   - `--profile-directory="Profile 2"`
   - `--remote-debugging-port=9222`
   - `--remote-allow-origins=*`
   - (pas de `--user-data-dir` explicite car le profil est résolu via `Local State`)
5. Attend activement que `http://127.0.0.1:9222/json/version` répond (jusqu'à 6 secondes)

## Règles d'or

- **Interdiction formelle de lancer `chrome.exe` manuellement** sans passer par cette compétence (ou `webx session start` depuis WEBX L2-PLATFORM).
- **Toujours vérifier** `http://127.0.0.1:9222/json/version` après lancement.
- **Ne jamais tuer** une instance Chromium déjà ouverte (`taskkill /IM chrome.exe` interdit).
- **Profil 2 uniquement** — pas de profil "Default", pas de profil temporaire.

## Codes de sortie

| Code | Signification |
|------|---------------|
| 0 | Chromium Profil 2 opérationnel sur le port 9222 |
| 1 | Erreur : dossier Profil 2 introuvable, échec WMI, ou port non réponse |

## Exemple d'usage

```powershell
# Depuis ENV3-repo ou tout agent de l'écosystème
pwsh -File "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\navigation-web\cdp\launch-chromium-profile2\scripts\launch_profile2_wrapper.ps1"
```

## Vérification post-lancement

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 2
```

Doit retourner un objet JSON avec `Browser`, `Protocol-Version`, `User-Agent`, etc.

## Référence ADR

- **ADR** : ADR-ENV2-010 (cadre M3 Tree/Branch pour extensions), ADR-20261112-01 (risque CDP)
- **IntentHash** : 0xSKILL_LAUNCH_CHROMIUM_PROFILE2_20261126
- **WAL** : WAL-0x243
