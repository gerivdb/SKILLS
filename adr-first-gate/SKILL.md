# Skill : adr-first-gate

## Déclencheurs

- Avant toute création de fichier ADR (.md avec frontmatter ADR).
- Avant toute modification d'un fichier ADR existant.
- Avant toute création de composant N+1 (nouveau stratum, nouveau système, nouveau citizen).
- Avant toute modification d'un document constitutionnel (ADR, EPIC, PRD qui définit l'architecture).

## Règles (numérotées, impératives)

1. Avant toute création ou modification d'un document de gouvernance (ADR, EPIC, PRD, INTENT qui touche l'architecture), vérifier qu'un ADR backing existe et est en statut `accepted`.
2. Si le statut est `proposed`, demander confirmation HITL avant de passer à `accepted`.
3. Interdit de passer un statut de `proposed` à `accepted` soi-même sans approbation explicite.
4. Avant toute création d'un Citizen, d'un composant N+1, ou de tout élément architectural, vérifier que l'ADR de référence existe et est accepté.
5. Ne pas créer de nouveau composant si un composant existant couvre déjà le besoin (voir aussi `skill-router-enforcement`).

## Anti-patterns (interdits documentés)

- Créer un ADR en statut `accepted` sans approbation explicite d'un utilisateur humain.
- Passer un ADR de `proposed` à `accepted` soi-même sans approbation.
- Créer un composant N+1 sans ADR backing.
- Créer un nouveau composant quand un composant existant couvre déjà le besoin.

## Preuve de vie

- `Test-Path` sur le fichier ADR référencé.
- Preuve que le statut de l'ADR est `accepted` (lecture du frontmatter YAML).
- Journalisation de la demande d'approbation et de la réponse de l'utilisateur.

## Configuration

Aucun paramètre configurable. Les chemins et dépendances dépendent du contexte d'exécution.
