---
name: triade-iris
description: "IRIS external sensor, polling, GitHub Actions workflow, target YAML. Use when user mentions 'IRIS', 'polling', 'capteur externe'."
---
|
# Triade IRIS

## Domaine et périmètre

La Triade Cognitive est le pipeline de veille et d'assimilation. Ce skill couvre :
- IRIS : le capteur externe qui surveille les dépôts
- Le polling via GitHub Actions
- La configuration des cibles YAML

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier les permissions Settings Actions du dépôt cible.
- Contrôler les scopes du GITHUB_TOKEN.
- Inspecter les logs des derniers runs IRIS.

### Phase 2 : Configuration
- Éditer le fichier YAML de la cible dans gerivdb/Gitnote/clusters/reposignal/targets/.
- Définir le dépôt externe, les patterns regex, la fréquence de polling.
- Activer le workflow iris-poll.yml.

### Phase 3 : Exécution
- Déclencher un test manuel ou attendre le cron.
- Vérifier que les signaux bruts sont bien poussés vers KRONOS.
- Diagnostiquer un startup_failure si nécessaire (souvent un problème de permissions).

## Règles de décision
- **Règle 1** : Un startup_failure en < 2s = problème de permissions Settings.
- **Règle 2** : Respecter les rate-limits GitHub (1 appel par seconde minimum).
- **Règle 3** : Les cibles inactives depuis 30 jours sont désactivées.

## Format de sortie

```markdown
## Statut IRIS
- Cible : oven-sh/bun
- Dernier run : succès (il y a 2h)
- Signaux détectés : 3
```

## Exemples d'utilisation
- "Ajoute une surveillance sur le dépôt X" → Créer le YAML cible.
- "Diagnostique un startup_failure sur IRIS" → Vérifier les permissions.

## Intégration avec l'écosystème
- Dépôts concernés : IRIS, KRONOS, Gitnote
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS]
