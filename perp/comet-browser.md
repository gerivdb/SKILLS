---
name: comet-browser
description: Browser automation and extension expert for COMET, comet-devcomet-extension, BIRDY. Use when user mentions
  "COMET", "BIRDY", "extension", "navigateur", "CDP", "automation browser", "comet-devcomet".
---

# Comet Browser

## Instructions

1. **Identifier la demande** : intégration protocole COMET, debug extension, API COMET, fragments de pages.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/COMET` ou `gerivdb/comet-devcomet-extension`.
3. **Vérifier le mode CDP** (full/partial/none) avant toute commande — COMET supporte CDP partiellement (HTTP 405 sur Target.createTarget).
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Ne pas supposer que Target.createTarget fonctionne — utiliser le mode dégradé auto-détection.
- BIRDY est un fork Ladybird 243 avec FFI Rust↔Go, ne pas confondre avec COMET.
- Toute automation browser doit passer par ENV5 (bridge Playwright).

## Format

- Code fences pour les commandes CDP et API COMET.
- Listes pour les étapes de debug extension.

## Exemples

- "[Récupérer le contenu de l'onglet actif via COMET]" → Vérifier mode CDP, appeler API COMET port ENV5, retourner fragment structuré.
