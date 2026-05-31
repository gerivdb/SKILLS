---
name: reposcope-watch
description: "External surveillance: signals, flags, env vars, API endpoints, secrets. Use when user mentions 'surveillance', 'signal', 'hidden flag', 'API endpoint', 'secret CI'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# RepoScope Watch

## Domaine et périmètre

RepoScope Watch est le module de **surveillance des dépôts externes**. Skill couvre :
- La configuration des cibles de surveillance (fichiers YAML)
- Le polling GitHub API (commits, PRs, issues) via IRIS
- L'extraction des signaux (API endpoints, flags, variables env, secrets CI)
- La détection de changements (nouveaux flags, endpoints modifiés, secrets exposés)

## Méthodologie

### Phase 1 : Configuration de la cible
- Lire le fichier YAML dans `gerivdb/Gitnote/clusters/reposignal/targets/`.
- Vérifier les patterns regex (URLs d'API, flags CLI, variables d'environnement).
- Ajuster les patterns si nécessaire.

### Phase 2 : Surveillance
- Polling GitHub API sur le dépôt externe via IRIS.
- Appliquer les patterns d'extraction sur chaque commit/PR.
- Stocker les signaux bruts détectés.

### Phase 3 : Qualification
- Transmettre les signaux à KRONOS pour scoring.
- Publier les signaux qualifiés via RepoScope Publish.
- Mettre à jour la timeline de découverte.

## Règles de décision
- **Règle 1** : Un flag non documenté mais activable = MEDIUM ; utilisé dans des tests = HIGH.
- **Règle 2** : Les secrets exposés en clair sont une alerte immédiate (HIGH).
- **Règle 3** : Les cibles inactives depuis 30 jours sont désactivées.

## Format de sortie

```markdown
## Surveillance [cible]
- Dernier poll : [date]
- Signaux détectés : [N]
- Nouveaux : [N]
- Alertes HIGH : [N]
```

## Exemples d'utilisation
- "Surveille oven-sh/bun pour de nouveaux flags" → Configurer et poller.
- "Ajoute une surveillance sur le dépôt X" → Créer le YAML cible.
- "Quels signaux ont été détectés hier ?" → Lister les résultats.

## Intégration avec l'écosystème
- Dépôts concernés : Gitnote, IRIS, KRONOS, NEXUS
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
