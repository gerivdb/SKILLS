---
name: triade-mind
description: Cognitive triad expert for IRIS, KRONOS and FLUX pipeline. Use when user mentions
  "IRIS", "KRONOS", "FLUX", "triade cognitive", "signal", "poll", "startup_failure".
---

# Triade Mind

## Instructions

1. **Identifier la demande** : poll de signaux, diagnostic startup_failure, test end-to-end, revue HITL.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/IRIS`, `gerivdb/KRONOS`, `gerivdb/FLUX` selon le contexte.
3. **Vérifier les tokens GITHUB** et permissions de workflow avant toute action CI.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Ne jamais inventer un endpoint ou un format de signal sans l'avoir lu dans le code.
- Les imports PYTHONPATH doivent être vérifiés avant de diagnostiquer un échec.
- Toute revue HITL doit être tracée avant clôture.

## Format

- Listes pour les étapes de diagnostic.
- Code fences pour les commandes et logs.

## Exemples

- "[KRONOS ne démarre pas]" → Vérifier `gerivdb/KRONOS` logs GitHub Actions, contrôler PYTHONPATH et token GITHUB, proposer le fix.
