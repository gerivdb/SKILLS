---
name: hitl-ops
description: HITL operations, governance audit and ecosystem health expert. Use when user mentions
  "HITL", "audit", "gouvernance transverse", "token scope", "permissions", "rapport d'état", "ECOS_ROOT", "priorisation".
---
|


# HITL Ops

## Instructions

1. **Identifier la demande** : actions HITL restantes, audit branches, permissions GitHub Actions, rapport d'état écosystème.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/NEXUS/ECOS_ROOT.json` puis logs KIVA si besoin.
3. **Croiser ECOS_ROOT + registres NEXUS** pour prioriser les tâches par criticité φ-CPS.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Aucune action de merge ou commit sans GO HITL explicite — règle absolue NEXUS.
- Les scopes de token GitHub doivent être vérifiés avant tout diagnostic de permission.
- Un rapport d'état sans SHA courant NEXUS est `[DÉRIVÉ]` et doit être marqué comme tel.

## Format

- Tableaux pour les actions HITL priorisées par criticité.
- Listes pour les recommandations de scopes token.

## Exemples

- "[Générer le rapport d'état de l'écosystème]" → Lire ECOS_ROOT.json, croiser avec logs KIVA, afficher tableau repos par statut φ-CPS avec actions HITL prioritaires.

