# Skill: untracked-auditor

## Contexte
Des fichiers untracked préexistent dans un repo (travail précédent non commité, fichiers générés). Ils risquent d'être mélangés à un commit ciblé ou oubliés dans la dette.

## Règle
Avant tout `git add` :
1. Exécuter `git status --short` et compter les `??`
2. Si untracked > 0, lister les chemins
3. Vérifier si ces fichiers sont référencés dans un EPIC/PRD existant
4. Si oui : proposer de les ajouter au commit courant avec message dédié
5. Si non : émettre alerte `UNTRACKED_DEBT` et demander instruction (add/ignore/delete)
6. Ne jamais créer de fichier dans un répertoire où des untracked non liés existent sans clarification

## Anti-pattern interdit
- Ignorer les untracked et créer de nouveaux fichiers dans le même répertoire
- Faire `git add .` pour "ranger" les untracked
- Supprimer des untracked sans confirmation

## Exemple d'application
```
KIVA-CLI : git status --short
?? cli/commands/review.py
?? cli/commands/tql.py
→ Non référencés dans EPIC métacluster PR
→ Alerte UNTRACKED_DEBT émise
→ Instruction demandée : add/ignore/delete
→ Pas de création de fichier dans cli/commands/ sans clarification
```
