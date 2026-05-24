---
name: data-vector
description: Data, vector and visualization expert for VDB, DATA-MINER, ECOS-VISION. Use when user mentions
  "VDB", "DATA-MINER", "ECOS-VISION", "TQL", "vecteur", "embedding", "similarité", "VEC-243".
---

# Data Vector

## Instructions

1. **Identifier la demande** : requête TQL, analyse similarité, certification VEC-243, génération embeddings.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/VDB` ou `gerivdb/DATA-MINER` selon le contexte.
3. **Lire le schéma TQL** avant de traduire une requête utilisateur.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Ne jamais inventer un endpoint VDB sans l'avoir lu dans le code source.
- Les requêtes hybrides SparrowDB+VDB doivent respecter le schéma de jointure canonique.
- La certification VEC-243 est obligatoire avant tout déploiement vectoriel en production.

## Format

- Code fences pour les requêtes TQL et exemples hybrides.
- Tableaux pour les scores de similarité.

## Exemples

- "[Trouver les 5 documents les plus proches de ce signal]" → Générer requête TQL, appeler VDB, afficher tableau de scores de similarité.
