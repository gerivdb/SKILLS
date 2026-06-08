---
name: plix-core
version: "2.0.0"
description: "PLIX video substrate, CODEC-243, PLAYER-243, PLIXVAULT, OCTOPUS, BitNet mapping, ThermoGate, VDB. Use when user mentions 'PLIX', 'CODEC-243', 'PLAYER-243', 'PLIXVAULT', 'OCTOPUS', 'ThermoGate', 'VDB'."
triggers: ["PLIX", "CODEC-243", "PLAYER-243", "PLIXVAULT", "OCTOPUS", "ThermoGate", "VDB"]
layer: "L3_EMERGENCE"
nexusTags: ["CONFORME_NEXUS", "DÉRIVÉ"]
prerequisites: []
slotWeight: 1
status: active
changelog:
  - {v: "2.0.0", date: "2026-05-30", notes: "Ajout couverture ThermoGate et VDB"}
trit_primitive: TritDocumentClassify
---
# PLIX Core

## Domaine et périmètre

PLIX est le **substrat vidéo ternaire** de l'écosystème. Ce skill couvre :
- PLIX (substrat brut, PLIXVAULT, API)
- CODEC-243 (quantification 2D, RHT, stochastic rounding)
- PLAYER-243 (lecteur/navigateur PLIXVAULT)
- VEC-243 (certification vectorielle)
- Le mapping BitNet b1.58 et l'architecture Adobe-like
- **ThermoGate** : gestion des seuils de température et déclenchement d'actions de refroidissement ou de performance.
- **VDB** (Vector Database) : stockage et recherche de vecteurs haute dimension pour les embeddings temporels et spatiaux.

## Méthodologie

### Phase 1 : Compréhension du besoin
- Identifier le composant PLIX concerné.
- Vérifier l'état d'avancement (Phases 0-8).
- Consulter le PRD PLIX Suite v2.

### Phase 2 : Analyse technique
- Expliquer le fonctionnement (pentades, frames, GOP).
- Faire le lien avec le matériel Z600 (CPU-only, 24 GB RAM).
- Proposer des optimisations (compression, navigation).
- **ThermoGate** : décrire les algorithmes de hysteresis, les points de consigne et les actions de déclenchement (réduction du framerate, activation du ventilateur).
- **VDB** : expliquer les métriques de similarité (cosine, euclidien), les algorithmes d'indexation (IVF, HNSW) et les cas d'utilisation (recherche de frames similaires, détection d'anomalies).

## Règles de décision
- **Règle 1** : PLIX est ternaire (3⁵ = 243 états par canal) — ne pas confondre avec du binaire.
- **Règle 2** : Toujours vérifier la compatibilité CPU (pas de GPU requis).
- **Règle 3** : Les benchmarks de compression sont la métrique clé.
- **Règle 4** (ThermoGate) : Si la température dépasse le seuil critique pendant plus de 5 s, activer le mode de dégradation gracefull.
- **Règle 5** (VDB) : Utiliser un index approximatif lorsque le nombre de vecteurs dépasse 1 M pour maintenir une latence < 10 ms.

## Format de sortie

```markdown
## Récapitulatif PLIX
- Dépôt : ...
- Statut : ...
- Prochaine étape : ...
```

## Exemples d'utilisation
- "Fais un récapitulatif de PLIX" → Structure et roadmap.
- "Explique le mapping BitNet dans PLIX" → Décrire les pentades.
- "Optimise CODEC-243 pour le Z600" → Proposer des améliorations.
- "Configurer ThermoGate pour le Z600" → Définir les points de consigne et les actions de déclenchement.
- "Interroger la VDB pour trouver les frames les plus similaires à une donnée" → Utiliser la requête de similarité cosinus avec seuil 0.85.

## Intégration avec l'écosystème
- Dépôts concernés : PLIX, CODEC-243, PLAYER-243, VEC-243, GOV-243
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [DÉRIVÉ]