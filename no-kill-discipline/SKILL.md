# Skill : no-kill-discipline

## Déclencheurs
- Avant toute commande `kill`, `taskkill`, `Stop-Process`, `killall`
- Avant toute suppression de processus (chrome.exe, powershell.exe, python.exe, etc.)
- Avant toute suppression d'un processus enfant (enfant d'un shard, d'un test, d'un serveur, d'un navigateur)

## Règles (numérotées, impératives)

1. Avant toute suppression de processus, vérifier que le PID appartient au processus lancé par soi-même (et non par un autre shard ou par l'utilisateur).
2. Vérifier qu'aucun autre shard n'utilise le processus (Vérifier `Get-Process`, `netstat` pour les ports occupés, liste des worktrees actifs).
3. Interdit d'utiliser `taskkill /IM chrome.exe` ou `taskkill /IM python.exe` sans spécifier le PID exact du processus à tuer.
4. Utiliser `Stop-Process -Id <PID> -Force` (arrêt propre) plutôt que `taskkill /F` (arrêt brutal).
5. Après toute suppression, vérifier que le processus est bien terminé et que le port qu'il utilisait est libéré.

## Anti-patterns (interdits documentés)

- `taskkill /IM chrome.exe` — tue TOUTES les instances Chrome, y compris celles d'autres shards ou de l'utilisateur.
- `taskkill /IM powershell.exe` — tue TOUTES les sessions PowerShell, y compris celles d'autres shards.
- `taskkill /IM python.exe` — tue TOUTES les instances Python, y compris celles d'autres shards.
- `killall chrome` — même effet que `taskkill /IM chrome.exe`.
- `Stop-Process -Name chrome` — même effet.
- Tuer un processus dont on ne connaît pas le PID exact.
- Tuer un processus sans vérifier qu'il n'appartient pas à un autre shard (shard A, B, C, D, E).

## Preuve de vie

- `Test-Path` sur le répertoire de travail du processus tué (doit encore exister ou avoir été légitimement supprimé).
- `Get-Process | Where-Object {$_.Name -eq "chrome"}` — ne doit plus contenir le PID tué.
- `netstat -ano | findstr :<port>` — confirme que le port utilisé par le processus tué est libéré.

## Configuration

Aucun paramètre configurable. Les chemins et dépendances dépendent du contexte d'exécution.
