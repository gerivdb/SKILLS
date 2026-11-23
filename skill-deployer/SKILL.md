# Skill: skill-deployer

## Description
Déploie un skill d'un dépôt source vers un dépôt cible (ex: de `SKILLS` vers `DevTools` ou `ENV3-repo`). Vérifie la compatibilité du chemin de destination, écrit le WAL de déploiement, et vérifie l'intégrité après copie.

## Déclencheurs
- Mentions : "déployer skill", "installer skill", "copier skill vers repo"

## Règles
- Le chemin de destination doit être dans une strate L* valide (L0-L6)
- Aucun chemin hors strate n'est autorisé
- Un WAL d'entrée est écrit après chaque déploiement
- Le skill déployé doit passer le `skill-linter-sentinel` avant activation

## Invariants
- Aucun déploiement hors strate L* n'est autorisé
- Aucun déploiement sans vérification du skill-linter-sentinel
- Chaque déploiement génère une entrée WAL

## Statut
- Version : 1.0.0
- Statut : active
- Type : domain
- Dépendances : `skill-linter-sentinel`