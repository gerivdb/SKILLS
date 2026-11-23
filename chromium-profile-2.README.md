# chromium-profile-2 — Skill spécialisé Profil 2 avec CDP

## Problème résolu

Le skill `chromium-durable-profile.psm1` ouvre `--user-data-dir` sans jamais passer `--profile-directory`.
Résultat : Chromium ouvre systématiquement le profil "Default", jamais "Profile 2".
Ce skill corrige définitivement ce défaut.

## Profil cible (durci)

| Élément | Valeur |
|---------|--------|
| user-data-dir | `C:\Users\GG\AppData\Local\Chromium\User Data` |
| profile-directory | `Profile 2` |
| Executable | `C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe` |
| CDP address | `127.0.0.1` (jamais 0.0.0.0) |
| CDP port | `9222` |

## Fonctions

| Fonction | Rôle |
|----------|------|
| `Test-ChromiumProfile2Cdp` | Vérifie que CDP répond sur 127.0.0.1:9222 |
| `Start-ChromiumProfile2` | Lance le Profil 2 avec CDP (inclut --profile-directory=Profile 2) |
| `Ensure-ChromiumProfile2` | Lance si inactif, sinon retourne le statut existant |
| `Get-ChromiumProfile2Targets` | Liste les cibles CDP du Profil 2 |
| `Get-ChromiumProfile2TargetByUrl -UrlPattern '*gemini*'` | Cible par pattern d'URL |
| `Open-ChromiumProfile2Page -Url <str>` | Ouvre une URL dans un nouvel onglet CDP |
| `Close-ChromiumProfile2Target -TargetId <str>` | Ferme une cible CDP |

## Usage

```powershell
Import-Module "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2.psm1"

# Garantir que le Profil 2 est actif avec CDP
$status = Ensure-ChromiumProfile2

# Ouvrir Gemini dans le Profil 2
$tab = Open-ChromiumProfile2Page -Url "https://gemini.google.com/app"

# Fermer l'onglet
Close-ChromiumProfile2Target -TargetId $tab.targetId
```

## Règles de sécurité (BDCP)

- CDP bindé strictement sur `127.0.0.1` (jamais `0.0.0.0`)
- En-têtes `Authorization`, `Cookie`, `Set-Cookie` filtrés dans toutes les sorties
- Aucun cookie/token en clair dans les fichiers de sortie
- Aucun screenshot collé dans le transcript

## Pourquoi ce skill existe

Le skill générique `chromium-durable-profile.psm1` ne passe JAMAIS `--profile-directory`.
Sans ce flag, Chromium ouvre le profil "Default" et ignore "Profile 2".
Ce skill est la correction permanente. Ne pas dupliquer ailleurs.
