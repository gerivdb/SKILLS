---
name: triade-kronos
description: "KRONOS digester, signal qualification, deduplication. Use when user mentions 'KRONOS', 'digesteur', 'qualification'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritNotify
---
# Triade KRONOS

## Domaine et périmètre

La Triade Cognitive est le pipeline de veille et d'assimilation. Ce skill couvre :
- KRONOS : le digesteur qui qualifie les signaux bruts
- La déduplication et le pré-scoring
- La transmission vers FLUX pour review

## Méthodologie

### Phase 1 : Réception
- Récupérer les signaux bruts émis par IRIS.
- Vérifier l'intégrité des données (commit_sha, fragment, source).
- Stocker temporairement dans la file d'attente KRONOS.

### Phase 2 : Qualification
- Dédupliquer : éliminer les signaux déjà traités (même commit_sha + même fragment).
- Calculer un score de confiance préliminaire (HIGH/MEDIUM/LOW) selon les patterns.
- Enrichir avec des métadonnées (timestamp, auteur du commit).

### Phase 3 : Transmission
- Pousser les signaux qualifiés vers FLUX pour review.
- Mettre à jour le registre des signaux traités.
- Logger les statistiques (nombre de signaux, doublons, scores).

## Règles de décision
- **Règle 1** : Les signaux déjà vus (même commit_sha + même fragment) sont systématiquement dédupliqués.
- **Règle 2** : Un flag non documenté → MEDIUM ; un secret exposé → HIGH.
- **Règle 3** : Les signaux avec un score LOW sont conservés 7 jours en file d'attente.

## Format de sortie

```markdown
## Traitement KRONOS
- Signaux reçus : 12
- Doublons éliminés : 2
- Qualifiés : 10 (HIGH: 1, MEDIUM: 5, LOW: 4)
- Transmis à FLUX : 10
```

## Exemples d'utilisation
- "Quels signaux sont en attente dans KRONOS ?" → Lister la file d'attente.
- "Déduplique les signaux du lot #42" → Lancer la déduplication.

## Intégration avec l'écosystème
- Dépôts concernés : KRONOS, IRIS, FLUX
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS]
