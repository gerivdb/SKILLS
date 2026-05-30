---
name: data-vector
description: "VDB, TQL, embeddings, vector search, VEC-243, SparrowDB. Use when user mentions 'VDB', 'TQL', 'embedding', 'vector', 'VEC-243'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# Data Vector

## Domaine et périmètre

Ce skill couvre la gestion des **données vectorielles** dans l'écosystème gerivdb :
- VDB (Vector Database) : stockage et recherche de vecteurs
- TQL (Ternary Query Language) : langage de requête pour données ternaires
- Embeddings (nomic-embed-text, 768 dimensions)
- VEC-243 : certification vectorielle en base 243
- SparrowDB : base de données légère embarquée

## Méthodologie

### Phase 1 : Identification du besoin
- Déterminer le type d'opération : indexation, recherche, certification.
- Identifier la source de données (texte, image PLIX, code).
- Choisir le modèle d'embedding (nomic-embed-text pour texte, VEC-243 pour ternaire).

### Phase 2 : Traitement
- Générer les embeddings via le modèle approprié.
- Indexer dans VDB (ou SparrowDB pour les cas légers).
- Optimiser les index (HNSW, IVF) selon le volume.

### Phase 3 : Recherche et validation
- Exécuter la requête (TQL pour ternaire, SQL-like pour VDB).
- Évaluer la pertinence des résultats (score de similarité cosinus).
- Certifier via VEC-243 si requis.

## Règles de décision
- **Règle 1** : nomic-embed-text (768-dim) pour tout ce qui est texte.
- **Règle 2** : VEC-243 pour les données PLIX (ternaire, pentades).
- **Règle 3** : SparrowDB pour les volumes < 10k vecteurs, VDB pour le reste.

## Format de sortie

```markdown
## Résultat vectoriel
- Requête : [texte/vecteur]
- Résultats : [N] (top 5)
- Scores : [liste]
- Certification VEC-243 : [valide | invalide]
```

## Exemples d'utilisation
- "Recherche les vecteurs similaires à cette description" → Recherche cosinus.
- "Indexe les embeddings de FLUENCE" → Générer et stocker.
- "Certifie ce vecteur VEC-243" → Valider la conformité ternaire.

## Intégration avec l'écosystème
- Dépôts concernés : VDB, VEC-243, PLIX, INTENT-ENCODER
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS]
