---
skill_id: contextual-stash-manager
trit_primitive: TritObserve
version: 1.1.0
updated: 2026-06-09
status: active
tags: [git, stash, context, workflow, contamination]
---

# contextual-stash-manager

## Purpose
Gérer les stashes Git par contexte de tâche pour éviter la contamination de commits.

## Trigger
Use when: user mentions "stash", "git stash", "contexte", "contamination", or when `git status` shows files outside current task scope.

## Steps

1. **Avant de stasher** — vérifier l'étendue :
   ```powershell
   git status --short
   ```

2. **Si > 5 fichiers hors périmètre** → stash obligatoire :
   ```powershell
   git stash push -m "EPIC-C-20260606-orphan-refs-wip"
   ```

3. **Format de nommage** : `<EPIC-ID>-<date>-<description>`
   - Exemple: `P15-20260609-skills-sync-wip`

4. **Pour restaurer** :
   ```powershell
   git stash list
   git stash apply stash@{N}
   ```

5. **Après validation** — supprimer le stash :
   ```powershell
   git stash drop stash@{N}
   ```

## Rules
- If `git status` shows > 5 files outside task scope → stash mandatory before commit
- Context purity threshold: `context_purity_score < 80%` (in-scope / total modified)
- Never `git add .` without verifying scope first
- Always name stashes with context prefix

## Output
- Named stash created/restored/dropped
- Clean working tree for current task scope

## Example

```powershell
# Working on P15 skills sync, but status shows unrelated changes
git status --short
# → M ../unrelated/file.txt
# → M perplexity/skills/win-unix-adapter.md
# → M perplexity/skills/git-lock-resolver.md

# Stash unrelated changes
git stash push -m "P15-20260609-unrelated-wip" ../unrelated/file.txt

# Now commit only P15 files
git add perplexity/skills/win-unix-adapter.md perplexity/skills/git-lock-resolver.md
git commit -m "feat(skills): P15 — enrich win-unix-adapter + git-lock-resolver"

# Restore unrelated work
git stash pop
```

## Integration
Called by `WORKSPACE-SANITIZER-DAEMON` before any push.
