---
name: reposcope-run
description: "Digestion engine execution, long scans, ingestion pipeline. Use when user mentions 'digestion', 'scan long', 'ingestion', 'pipeline'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# RepoScope Run

## Domaine et périmètre

RepoScope est le moteur de veille externe. Ce skill couvre :
- L'exécution de scans longs (polling de dépôts)
- Le pipeline d'ingestion des commits et PRs
- L'orchestration des étapes de digestion

## Méthodologie

### Phase 1 : Initialisation
- Charger les cibles depuis gerivdb/Gitnote/clusters/reposignal/targets/.
- Vérifier la connectivité GitHub API (rate-limit, token).
- Déterminer la fenêtre de scan (depuis le dernier run).

### Phase 2 : Exécution
- Pour chaque cible, itérer sur les commits récents via mcp_github.
- Appliquer les patterns d'extraction (regex).
- Stocker les signaux bruts dans une file d'attente.

### Phase 3 : Finalisation
- Lancer la qualification (appeler reposcope-process).
- Publier les signaux qualifiés (appeler reposcope-publish).
- Mettre à jour le timestamp du dernier run.

## Règles de décision
- **Règle 1** : Espacer les scans d'au moins 1 heure pour respecter les rate-limits.
- **Règle 2** : Si le token est expiré, arrêter et notifier.
- **Règle 3** : Un scan qui échoue 3 fois de suite → désactiver la cible.

## Format de sortie

```markdown
## Rapport d'exécution
- Cibles scannées : 3/3
- Signaux bruts : 12
- Signaux qualifiés : 5 (HIGH: 1, MEDIUM: 3, LOW: 1)
- Durée : 45s
```

## Exemples d'utilisation
- "Lance un scan complet de toutes les cibles" → Exécuter le pipeline.
- "Reprends le scan interrompu sur Bun" → Scan incrémental.

## Intégration avec l'écosystème
- Dépôts concernés : Gitnote, NEXUS, BRAIN
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS]
