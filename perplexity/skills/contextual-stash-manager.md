# contextual-stash-manager

## Objectif
Gérer les stashes Git par contexte de tâche pour éviter la contamination de commits.

## Principe
Chaque stash est nommé par contexte : `<EPIC-ID>-<date>-<description>`

## Commandes

```powershell
# Créer stash nommé
git stash push -m "EPIC-C-20260606-orphan-refs-wip"

# Lister stashes avec contexte
git stash list

# Restaurer stash spécifique
git stash apply stash@{N}

# Supprimer stash après validation
git stash drop stash@{N}
```

## Règle de contamination
- Si `git status` montre > 5 fichiers hors périmètre de la tâche courante → stash obligatoire avant commit
- Seuil d'alerte : `context_purity_score < 80%` (fichiers in-scope / total modifiés)
- Ne jamais `git add .` sans vérification préalable du périmètre

## Intégration
Appelé par `WORKSPACE-SANITIZER-DAEMON` avant tout push.
