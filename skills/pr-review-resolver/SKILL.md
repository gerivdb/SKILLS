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

# pr-review-resolver - Skill transverse universel

## Declencheur
Commande utilisateur : `review resoud PR` ou `review resoud PR #<num>`

## Pipeline orchestre
1. **diffscope-review** -> Analyse diff + commentaires inline
2. **pr-lifecycle-gate** -> Verifie checks CI, merge si OK
3. **merge-conflict-resolver** -> Resout conflits si merge bloque
4. **session-closeout (D5)** -> Nettoyage branches locales/distantes + WAL update

## Portee
- Fonctionne sur **tous les depots** de `D:\DO\WEB`
- Detection automatique du repo courant via `git rev-parse --show-toplevel`
- Utilise `gitmcp` ou `gh CLI` pour operations GitHub
- Respecte les guards transversaux avant toute action

## Execution
```bash
# Invocation via commande Kilo
review resoud PR [#<num>] [--mode=review-only|auto-merge|interactive]
```

## Guards appliques
- `agent-budget-check` : Verifie RAM/CPU avant delegation
- `adr-governance-gate` : Bloque si merge impacte pattern cross-repo sans ADR
- `checkout-canonicality` : Verifie clone canonique (CTULU/ECOYSTEM)