---
trit_primitive: TritDocumentTrace
---
# git-lock-resolver

## Objectif
Détecter et résoudre automatiquement les problèmes de fichier lock Git (`index.lock`, `HEAD.lock`).

## Déclencheurs
- `fatal: Unable to create '.git/index.lock': File exists`
- Toute erreur Git mentionnant `.lock`

## Procédure
1. Vérifier qu'aucun processus Git n'est actif : `Get-Process git -ErrorAction SilentlyContinue`
2. Si aucun processus actif : `Remove-Item .git/index.lock -Force`
3. Logger l'incident dans WAL ARGUS event `GIT_LOCK_RESOLVED`
4. Relancer la commande Git échouée

## Règles
- Ne jamais supprimer le lock si un processus Git est actif
- Toujours logger avant suppression
- Si lock réappraît > 3x en session → ouvrir issue `GIT_LOCK_RECURRENT`

## Environnement
Windows/PowerShell (ENV2). Pas de `rm` — utiliser `Remove-Item`.
