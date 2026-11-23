# Skill : proof-of-life-discipline

## Déclencheurs

- Avant toute déclaration de "succès", "fini", "terminé", "CLOS".
- Avant toute déclaration de "problème résolu", "bug corrigé".
- Avant toute déclaration de "tâche terminée" sur un shard.

## Règles (numérotées, impératives)

1. Une opération n'est considérée terminée que si une preuve artefactuelle est produite (fichier, sortie de commande, lien vers document).
2. Interdit de déclarer "succès" sans preuve artefactuelle correspondante.
3. Interdit de dire "tout est prêt" sans avoir vérifié que le fichier existe et est lisible.
4. Les déclarations "PRD-MOC-XXX CLOS" doivent être accompagnées de la preuve d'exécution (commande lancée, sortie, fichier créé).
5. Les déclarations "PRD-MOC-XXX CLOS" doivent être accompagnées de preuves indépendantes (pas d'auto-déclaration sans preuve externe).

## Anti-patterns (interdits documentés)

- Déclarer "tout est prêt" sans avoir vérifié que le fichier existe et est lisible.
- Déclarer "CLOS" sur la base d'une affirmation orale sans preuve artefactuelle.
- Déclarer "succès" sur la base d'une intention non exécutée.
- Déclarer "tout est prêt" sans avoir vérifié que le fichier existe et est lisible.

## Preuve de vie

- `Test-Path` sur chaque artefact produit.
- `git status --short` montrant les fichiers modifiés.
- Sortie de commande capturée (stdout/stderr).
- Lien vers un document existant et accessible.

## Configuration

Aucun paramètre configurable.
