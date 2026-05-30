---
name: intent-bridge
description: "Neurosymbolic bridge: INTENT-ENCODER, nomic-embed-text, 768-dim, ECOS v3.0. Use when user mentions 'INTENT-ENCODER', 'neurosymbolique', 'nomic-embed-text', 'BOINC-LLM'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# Intent Bridge

## Domaine et périmètre

Ce skill couvre le **pont neurosymbolique** de l'écosystème gerivdb :
- INTENT-ENCODER (encodage des intentions en vecteurs sémantiques)
- nomic-embed-text (modèle d'embedding, 768 dimensions)
- ECOS v3.0 (architecture neurosymbolique)
- BOINC-LLM (inférence distribuée des embeddings)
- Lien entre symbolique (ontologie, règles) et connexionniste (embeddings, similarité)

## Méthodologie

### Phase 1 : Encodage de l'intention
- Recevoir la requête en langage naturel.
- Générer l'embedding via nomic-embed-text (768-dim).
- Rechercher les intentions similaires dans le cache sémantique.

### Phase 2 : Pont neurosymbolique
- Mapper l'embedding vers les termes ontologiques (ONTOLOGY).
- Appliquer les règles symboliques (ADR, REPO-STANDARDS).
- Combiner la similarité connexionniste avec la logique symbolique.

### Phase 3 : Décision
- Si similarité ≥ 0.85 ET règles symboliques conformes → réponse directe.
- Si conflit → escalader vers HITL.
- Si similarité < 0.85 → générer une nouvelle réponse et l'encoder.

## Règles de décision
- **Règle 1** : Le seuil de similarité cosinus pour un match = 0.85.
- **Règle 2** : Les termes doivent exister dans ONTOLOGY — sinon, les définir d'abord.
- **Règle 3** : En cas de conflit symbolique vs connexionniste, le symbolique prime.

## Format de sortie

```markdown
## Résultat Intent Bridge
- Intention encodée : [768-dim vector]
- Similarité : [X.XX]
- Termes ONTOLOGY matchés : [liste]
- Décision : [conforme | conflit | nouveau]
```

## Exemples d'utilisation
- "Encode cette intention en vecteur" → Générer l'embedding.
- "Trouve les intentions similaires à X" → Recherche cosinus.
- "Résous le conflit entre la règle ADR-0015 et le match sémantique" → Escalader.

## Intégration avec l'écosystème
- Dépôts concernés : INTENT-ENCODER, ONTOLOGY, VDB, BRAIN
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
