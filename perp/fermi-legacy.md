---
name: fermi-legacy
description: Legacy hardware and performance expert for FERMI-EVER, CodeDB-E5620, LYCOS. Use when user mentions
  "FERMI", "CodeDB-E5620", "LYCOS", "Xeon E5620", "GPU Fermi", "AVX", "LXC Z600", "SSE4.2".
---

# Fermi Legacy

## Instructions

1. **Identifier la demande** : compilation GPU Fermi, optimisation Xeon E5620, containers LXC sur Z600.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/FERMI-EVER` ou `gerivdb/CodeDB-E5620`.
3. **Vérifier l'absence d'AVX** sur E5620 avant toute recommandation d'optimisation — utiliser SSE4.2 uniquement.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Le Xeon E5620 ne supporte pas AVX — tout build doit utiliser le fallback SSE4.2.
- LYCOS est un fork CodeDB avec encodage FLUENCE matrix + compression Janus, ne pas confondre avec CodeDB standard.
- Les optimisations GPU Fermi sont limitées à CUDA Compute 2.x.

## Format

- Code fences pour les flags de compilation et commandes LXC.
- Listes pour les astuces de performance hardware.

## Exemples

- "[Compiler LYCOS pour E5620]" → Vérifier flags `-O3 -msse4.2 -mno-avx`, lire `CodeDB-E5620/Makefile`, proposer la commande corrigée.
