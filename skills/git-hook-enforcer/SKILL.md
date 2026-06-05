# Skill: git-hook-enforcer

## Contexte
Les hooks pre-commit/BRGS valident les statuts, les paths interdits et les prefixes de branche. Écrire du contenu sans connaître ces règles cause des échecs systématiques en fin de session.

## Règle
Avant toute opération d’écriture/commit dans un repo :
1. Vérifier `.git/hooks/pre-commit` ou `.githooks/pre-commit`
2. Vérifier `git config core.hooksPath` pour détecter un chemin custom
3. Lire le hook pour extraire les règles (statuts autorisés, paths interdits, prefix branches)
4. Exposer ces règles via `.kilo/hooks-rules.yaml` pour les autres skills
5. Si hook absent : émettre `HOOK_MISSING`
6. Si hook non lisible : émettre `HOOK_UNREADABLE`

## Extraction des règles
- **Statuts autorisés** : grep sur les enum/listes dans le hook
- **Paths interdits** : grep sur les chemins bloqués
- **Prefix branches** : grep sur les patterns de branche acceptés
- **Validators custom** : identifier les scripts appelés (ex: `validate_docs.py`)

## Anti-pattern interdit
- Écrire un PRD/EPIC sans avoir lu les règles du hook
- Tenter `git commit --no-verify` pour contourner un échec
- Ignorer un hook manquant et committer sans validation

## Exemple d'application
```
GOVERNANCE-HUB : .githooks/pre-commit présent
→ Règles extraites :
   - PRD status : draft|in_review|approved|archived
   - EPIC status : planned|active|completed|archived
   - Paths interdits : .archive/, *.tmp
→ .kilo/hooks-rules.yaml mis à jour
→ doc-status-validator peut maintenant valider en amont
→ Pas d’échec pre-commit
```
