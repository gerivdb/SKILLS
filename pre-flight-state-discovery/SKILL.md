# Skill : pre-flight-state-discovery

## Déclencheurs

- Avant toute création de fichier, dossier, ou processus.
- Avant toute vérification d'existence (ex: "le fichier existe-t-il ?").
- Avant toute opération de write, commit, push, deploy.
- Avant toute opération de merge, sync, déploiement.
- Avant toute opération sur un fichier de configuration, vérifier que le fichier existe et est lisible.

## Règles (numérotées, impératives)

1. Avant toute création de fichier ou dossier, vérifier que le fichier/dossier n'existe pas déjà (`Test-Path`).
2. Avant toute opération de suppression, vérifier que le fichier/dossier existe (`Test-Path`).
3. Avant toute opération sur un port, vérifier que le port n'est pas déjà utilisé (`netstat -ano | findstr :<port>`).
4. Avant toute opération sur un processus, vérifier que le processus existe et appartient à soi-même (`Get-Process -Id <PID>`).
5. Avant toute opération sur un dépôt git, vérifier l'état du working tree (`git status --short`, `git log --oneline -3`).
6. Avant toute opération sur un fichier de configuration, vérifier que le fichier existe et est lisible.

## Anti-patterns (interdits documentés)

- Conclure "n'existe pas" après une récursive timeout sans avoir testé le chemin direct (`Test-Path`).
- Créer un fichier sans vérifier qu'il n'existe pas déjà (risque d'écrasement).
- Opérer sur un port sans vérifier qu'il n'est pas déjà utilisé.
- Opérer sur un processus sans vérifier s'il appartient à un autre shard.
- Supprimer un fichier sans vérifier qu'il existe.

## Preuve de vie

- `Test-Path` sur chaque chemin ciblé avant opération.
- `git status --short` avant toute opération git.
- `netstat -ano | findstr :<port>` avant toute opération sur un port.

## Configuration

Aucun paramètre configurable. Les chemins et dépendances dépendent du contexte d'exécution.
