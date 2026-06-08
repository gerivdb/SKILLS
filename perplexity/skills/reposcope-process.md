---
name: reposcope-process
description: "Signal scoring, cross-artefact correlation, timeline, discovery sheets. Use when user mentions 'scoring', 'corrélation', 'timeline', 'fiche découverte'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritScanRegistry
---
# RepoScope Process

## Domaine et périmètre

RepoScope est le moteur de veille externe. Ce skill couvre :
- Le scoring et la qualification des signaux
- La corrélation entre artefacts (commits, PRs, issues)
- La génération de fiches de découverte et de timelines

## Méthodologie

### Phase 1 : Collecte
- Récupérer les signaux bruts depuis le cluster Gitnote.
- Appliquer les patterns d'extraction (API, flags, variables).
- Normaliser les données (source, commit_sha, fragment).

### Phase 2 : Scoring
- Calculer le score de confiance : HIGH, MEDIUM ou LOW.
- Critères : documenté ? utilisé en test ? exposition de secret ?
- Croiser les signaux entre artefacts (ex. commit + issue liée).

### Phase 3 : Livraison
- Générer une fiche de découverte Markdown structurée.
- Publier dans brain-feed si score ≥ MEDIUM.
- Mettre à jour la timeline du dépôt surveillé.

## Règles de décision
- **Règle 1** : Un flag non documenté mais activable = MEDIUM ; s'il est utilisé dans des tests = HIGH.
- **Règle 2** : Les secrets exposés en clair sont une alerte immédiate.
- **Règle 3** : Toute hypothèse non vérifiée → [HYPOTHÈSE_NON_CONFIRMÉE].

## Format de sortie

```yaml
signal_id: RS-YYYY-NNN
repo_source: owner/repo
commit_sha: abc1234
confidence: HIGH
tags: [api-change, undocumented]
nexus_status: PENDING_ASSIMILATION
```

## Exemples d'utilisation
- "Score les signaux du dépôt oven-sh/bun" → Appliquer les règles de scoring.
- "Génère la timeline des découvertes sur Bun" → Créer un tableau chronologique.

## Intégration avec l'écosystème
- Dépôts concernés : Gitnote, NEXUS, BRAIN
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
