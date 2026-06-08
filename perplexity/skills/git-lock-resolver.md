---
skill_id: git-lock-resolver
trit_primitive: TritDocumentTrace
version: 1.1.0
updated: 2026-06-09
status: active
tags: [git, lock, windows, powershell, env2]
---

# git-lock-resolver

## Purpose
Détecter et résoudre automatiquement les problèmes de fichier lock Git (`index.lock`, `HEAD.lock`).

## Trigger
Use when: `fatal: Unable to create '.git/index.lock': File exists`, any Git error mentioning `.lock`, or Git commands hang unexpectedly.

## Steps

1. **Vérifier processus Git actifs** :
   ```powershell
   Get-Process git -ErrorAction SilentlyContinue
   ```
2. **Si aucun processus actif** — supprimer le lock :
   ```powershell
   Remove-Item .git/index.lock -Force
   ```
3. **Logger l'incident** dans WAL ARGUS event `GIT_LOCK_RESOLVED`
4. **Relancer la commande Git** échouée
5. **Si lock réapparaît > 3x en session** → ouvrir issue `GIT_LOCK_RECURRENT`

## Rules
- Never delete lock if a Git process is active
- Always log before suppression
- If lock recurs > 3x → escalate to `GIT_LOCK_RECURRENT` issue
- On Windows/PowerShell: use `Remove-Item` — never use `rm`

## Output
- Lock file removed
- Git command re-executed successfully
- WAL event logged

## Example

```powershell
# Error: fatal: Unable to create '.git/index.lock': File exists

# Step 1: Check for active git processes
Get-Process git -ErrorAction SilentlyContinue
# → no output = no active processes

# Step 2: Remove lock
Remove-Item .git/index.lock -Force

# Step 3: Retry
git status
# → working tree clean
```
