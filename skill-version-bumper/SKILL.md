# Skill: skill-version-bumper

## Description
Incrémente automatiquement les numéros de version dans les fichiers `SKILL.md` et `REGISTRY.yaml` lorsqu'un skill est modifié. Garantit la cohérence du versioning V-4D (Major.Minor.Patch.Micro-Delta) à travers l'écosystème des skills.

## Déclencheurs
- Mentions : "bump version", "maj version", "incrémenter version", "nouvelle version skill"

## Règles de versioning
- **Major** : changement d'API ou de contrat d'entrée/sortie du skill
- **Minor** : nouvelle fonctionnalité compatible
- **Patch** : correction de bug sans changement d'API
- **Micro-Delta** : correction typographique, formatage, documentation

## Flux d'exécution
1. Lire le fichier `SKILL.md` cible
2. Extraire la version actuelle (format vX.Y.Z.W)
3. Incrémenter selon le type demandé
4. Mettre à jour `SKILL.md` et `REGISTRY.yaml`
5. Écrire un WAL de traçabilité

## Invariants
- Aucun skill ne peut avoir deux versions différentes dans `SKILL.md` et `REGISTRY.yaml`
- Le numéro de version doit toujours être au format `vX.Y.Z.W`

## Statut
- Version : 1.0.0
- Statut : active
- Type : domain
- Dépendances : aucun