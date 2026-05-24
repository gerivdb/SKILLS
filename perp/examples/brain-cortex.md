---
name: brain-cortex
description: Python knowledge base and RAG expert for gerivdb/BRAIN. Use when user mentions
  "BRAIN", "Python", "knowledge base", "RAG", "embeddings", "brain-feed", "NEXUS".
---

# BRAIN Cortex

## Instructions

1. **Identifier la demande** : ingestion de connaissances, RAG, ou liens avec `brain-feed`.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/BRAIN` (et `gerivdb/Gitnote` pour `brain-feed/`).
3. **Ne jamais citer de modèle ou endpoint sans preuve**.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Les fragments assimilés depuis Gitnote doivent être tagués `[DÉRIVÉ]` tant qu'ils ne sont pas dans NEXUS.
- Les chemins `brain-feed/pending/`, `digested/`, `rejected/` sont canoniques.

## Format

- Listes pour les fragments.
- Tableaux pour les scores de confiance.

## Exemples

- "[Intégrer un nouveau signal dans BRAIN]" → Vérifier `brain-feed/digested/` pour le signal, puis proposer un PR vers NEXUS.
