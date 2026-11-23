# chromium-durable-profile — Profil Chromium durable avec CDP (tout type de page)

## Problème résolu
Le skill `chromium-cdp.psm1` ne pilote qu'un CDP déjà ouvert par un processus externe. Aucun profil n'est lancé ni persistant : cookies, localStorage et authentification sont perdus à la fermeture du navigateur, forçant un clic HITL « Autoriser » à chaque nouvelle session/corridor.

Ce skill fournit un **profil Chromium durable** (`--user-data-dir`) avec CDP activé, réutilisable pour **n'importe quelle page** (pas seulement DeepSeek).

## Flags clés

| Flag | Rôle |
|------|------|
| `--remote-debugging-port=9222` | Active le CDP REST sur `http://localhost:9222` |
| `--user-data-dir=<chemin>` | Isole le profil (cookies, localStorage, session, extensions) — durable entre redémarrages |
| `--no-first-run` | Saute l'assistant de première exécution |
| `--no-default-browser-check` | Évite les popups navigateur par défaut |

## Fonctions

| Fonction | Rôle |
|----------|------|
| `Ensure-ChromiumProfile` | Lance Chromium si CDP inactif, sinon retourne le statut existant |
| `Start-ChromiumProfile` | Lance explicitement avec profil + CDP |
| `Test-ChromiumCdp` | Vérifie que le port CDP répond |
| `Get-ChromiumTargets` | Liste toutes les cibles CDP (headers sensibles filtrés) |
| `Get-ChromiumTargetByUrl -UrlPattern '*deepseek*'` | Récupère un target authentifié par pattern d'URL |
| `Open-ChromiumPage -Url <str>` | Ouvre une URL dans un nouvel onglet CDP |
| `Close-ChromiumTarget -TargetId <str>` | Ferme une cible CDP |

## Usage

```powershell
Import-Module "D:\DO\WEB\TOOLS\L0-CANON\SESSION-GATE\gas-pipeline\v4\chromium-durable-profile.psm1"

# 1. Garantir un profil actif (lance si nécessaire)
$status = Ensure-ChromiumProfile -ProfileDir "C:\Users\GG\AppData\Local\Chromium\PlaygroundProfile" -Port 9222

# 2. Trouver une page authentifiée (n'importe quel domaine)
$target = Get-ChromiumTargetByUrl -UrlPattern "*script.google.com*" -Port 9222
if ($target.found) {
  $target.webSocketDebuggerUrl  # pour Playwright connect_over_cdp
}

# 3. Ouvrir une nouvelle page
$tab = Open-ChromiumPage -Url "https://example.com" -Port 9222
```

## Règles de sécurité (BDCP / non-divulgation)

- **Jamais** de valeur de cookie, token Authorization, ou session ID en clair dans les preuves/fichiers de sortie.
- Les en-têtes `Authorization`, `Cookie`, `Set-Cookie` sont filtrés par `Filter-SensitiveHeaders` dans toutes les fonctions de lecture.
- Pas de screenshot collé dans le transcript.

## Persistance
Le profil persiste dans le `user-data-dir` spécifié. Les cookies et l'authentification survivent à la fermeture de Chromium. Un seul clic HITL « Autoriser » par domaine/profil suffit pour les sessions suivantes.
