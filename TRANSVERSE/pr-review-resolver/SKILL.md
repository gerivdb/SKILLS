---
name: pr-review-resolver
description: "Review + resolve PR via diffscope + auto-merge gate + cleanup across all ecosystem repos"
intent_hash: 0xPR_REVIEW_RESOLVE_UNIVERSAL_20260730
scope: ecosystem
guards:
  - agent-budget-check
  - adr-governance-gate
  - checkout-canonicality
---

# pr-review-resolver — Skill transverse universel

## Déclencheur
Commande utilisateur : `review résoud PR` ou `review résoud PR #<num>`

## Pipeline orchestré
1. **diffscope-review** → Analyse diff + commentaires inline
2. **pr-lifecycle-gate** → Vérifie checks CI, merge si OK
3. **merge-conflict-resolver** → Résout conflits si merge bloque
4. **session-closeout (D5)** → Nettoyage branches locales/distantes + WAL update

## Portée
- Fonctionne sur **tous les dépôts** de `D:\DO\WEB`
- Détection automatique du repo courant via `git rev-parse --show-toplevel`
- Utilise `gitmcp` ou `gh CLI` pour opérations GitHub
- Respecte les guards transversaux avant toute action

## Exécution
```bash
# Invocation via commande Kilo
review résoud PR [#<num>] [--mode=review-only|auto-merge|interactive]
```

## Guards appliqués
- `agent-budget-check` : Vérifie RAM/CPU avant délégation
- `adr-governance-gate` : Bloque si merge impacte pattern cross-repo sans ADR
- `checkout-canonicality` : Vérifie clone canonique (CTULU/ECOYSTEM)