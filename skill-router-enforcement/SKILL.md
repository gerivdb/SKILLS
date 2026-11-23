# Skill : skill-router-enforcement

## Déclencheurs

- Avant toute création de fichier, script, ou composant.
- Avant toute écriture de nouveau code qui duplique une fonctionnalité existante.
- Avant toute création de nouveau skill, outil, ou module.

## Règles (numérotées, impératives)

1. Avant toute création, consulter `known_repositories.yaml` et les compétences existantes dans `SKILLS/`.
2. Si un skill, script, ou composant existe déjà qui couvre le besoin, l'utiliser ou l'étendre au lieu de créer un nouveau.
3. Ne pas créer un fichier si un fichier existant couvre déjà le besoin.
4. Ne pas créer un skill si un skill existant couvre déjà le besoin.
5. Avant toute création, vérifier dans `known_repositories.yaml` si le composant existe déjà.

## Anti-patterns (interdits documentés)

- Créer un fichier `shard_manager.py` alors qu'un `agent_manager_bridge.py` existe déjà.
- Créer un skill de "gestion de shard" alors qu'un `branch-hygiene-auditor` existe déjà.
- Créer un outil de "gestion de branches" alors qu'un `worktree-hygiene-auditor` existe déjà.
- Créer un script de "détection de fichiers" alors qu'un `pre-flight-state-discovery` existe déjà.

## Preuve de vie

- `known_repositories.yaml` consulté et consultable.
- `SKILLS/` directory listé et consulté.
- Preuve que le composant existant a été réutilisé (ou qu'une raison justifie la création d'un nouveau).

## Configuration

Aucun paramètre configurable. Les chemins et dépendances dépendent du contexte d'exécution.
