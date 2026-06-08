---
trit_primitive: TritDocumentTrace
---
# git-workflow-automator

## Objectif
Automatiser le workflow pull-rebase-push standard en détectant les conflits avant qu'ils bloquent.

## Workflow standard ENV2

```powershell
# 1. Vérifier état local
git status --short

# 2. Si unstaged changes → stash nommé
git stash push -m "auto-stash-$(Get-Date -Format 'yyyyMMdd-HHmm')"

# 3. Pull rebase
git pull --rebase origin main

# 4. Si conflit rebase → abort + rapport
# git rebase --abort

# 5. Si clean → push
git push origin main

# 6. Restaurer stash si applicable
git stash pop
```

## Déclencheurs d'abort
- Conflit de merge non résolu → `git rebase --abort` + issue `REBASE_CONFLICT`
- Divergence > 10 commits → validation humaine obligatoire avant push

## Règle
Jamais de `git push --force` sans instruction explicite HITL.
