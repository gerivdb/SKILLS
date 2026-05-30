---
name: reposcope-publish
description: "Brain-feed publication, signal clustering, dashboards, alerts. Use when user mentions 'brain‑feed', 'clusters', 'dashboard', 'alertes'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# RepoScope Publish

## Domaine et périmètre

RepoScope est le moteur de veille externe. Ce skill couvre :
- La publication des signaux qualifiés dans brain-feed
- La création de clusters de signaux similaires
- La génération de dashboards et d'alertes

## Méthodologie

### Phase 1 : Sélection
- Filtrer les signaux avec confidence ≥ MEDIUM.
- Regrouper par dépôt source, puis par tag commun.
- Éliminer les doublons (même commit_sha et même fragment).

### Phase 2 : Publication
- Générer un fichier Markdown par cluster dans brain-feed/signals/.
- Mettre à jour l'index brain-feed/INDEX.md.
- Committer et pousser vers le dépôt Gitnote.

### Phase 3 : Notifications
- Déclencher une alerte si un signal HIGH est détecté (issue GitHub).
- Mettre à jour le dashboard NEXUS/registry-view.

## Règles de décision
- **Règle 1** : Un cluster de plus de 3 signaux similaires → créer une issue de suivi.
- **Règle 2** : Les secrets exposés déclenchent une alerte immédiate.
- **Règle 3** : Les signaux LOW restent en attente 7 jours avant suppression.

## Format de sortie

```markdown
## Nouveaux signaux publiés
| ID | Source | Confidence | Tag |
|----|--------|------------|-----|
| RS-2025-001 | oven-sh/bun | HIGH | hidden-flag |
```

## Exemples d'utilisation
- "Publie les signaux HIGH en attente" → Générer et pousser les fiches.
- "Crée un dashboard des signaux du mois" → Agréger les données.

## Intégration avec l'écosystème
- Dépôts concernés : Gitnote, NEXUS, BRAIN
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS]
