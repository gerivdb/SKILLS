---
type: skill
version: "1.0.0"
date: "2026-06-18"
intent_hash: 0xBRANCH_LIFECYCLE_INTENT_φ1.000
status: active
trit_primitive: TritTrackBranch
tags: [branch, lifecycle, intent, git-hygiene, l3-tooling]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "GIT_HYGIENE", "BRANCH_MANAGEMENT"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 clôture axe C — gap tracking cycle de vie branches avec intention"}
---

# branch-lifecycle-intent-tracker

## Purpose

Traque le **cycle de vie complet** d'une branche Git en l'associant à son intention d'origine (feature, fix, adr, refactor, hotfix) et déclenche les actions appropriées selon l'état courant. Complète `branch-cleaner` CTULU en ajoutant la dimension sémantique : une branche sans PR depuis > 30j **et** sans intent actif est candidate à la suppression ; une branche avec intent vivant est à protéger même orpheline.

## Trigger

Utiliser quand :
- une branche est créée, fusionnée ou supprimée sur `gerivdb/*`
- `list_branches` retourne > 10 branches sur un repo
- une PR est mergée et la branche source n'est pas auto-supprimée
- un audit de branches orphelines est demandé
- besoin de savoir si supprimer une branche est sûr

## États du cycle de vie

```
[CRÉÉE] → [ACTIVE] → [MERGÉE] → [ARCHIVÉE] → [SUPPRIMÉE]
            ↓
         [ABANDONNÉE] → [À_NETTOYER]
```

| État | Critères | Action recommandée |
|---|---|---|
| CRÉÉE | branch existe, 0 commit depuis fork | Vérifier si intent déclaré |
| ACTIVE | commits récents (≤ 7j) ou PR open | Protéger |
| MERGÉE | PR merged, branch non supprimée | Supprimer via mcp_github |
| ABANDONNÉE | > 30j sans commit, sans PR open | Audit intent avant suppression |
| À_NETTOYER | Abandonnée + pas d'intent vivant | Supprimer |
| ARCHIVÉE | Taguée, figée volontairement | Ne pas supprimer |

## Nomenclature des intentions

Convention de nommage attendue (RSS-v1) :

```
feature/{slug}     →  intent: NOUVELLE_FONCTIONNALITÉ
fix/{slug}         →  intent: CORRECTION_BUG
adr-{N}-{slug}     →  intent: DÉCISION_ARCHITECTURE
refactor/{slug}    →  intent: REFACTORING
hotfix/{slug}      →  intent: CORRECTIF_URGENCE
chore/{slug}       →  intent: MAINTENANCE
epic/{slug}        →  intent: EPIC_EN_COURS
```

Branche sans préfixe reconnu → intent: INCONNU → déclencher clarification avant suppression.

## Protocole de décision suppression

```
[BRANCH_TRACKER] Branche: {nom}
[BRANCH_TRACKER] Âge: {N} jours | Dernier commit: {date}
[BRANCH_TRACKER] PR associée: {numéro|aucune} | Statut PR: {open|merged|closed|aucune}
[BRANCH_TRACKER] Intent détecté: {intent} (depuis nom de branche)
[BRANCH_TRACKER] Intent vivant (issue/epic ouverte): {oui|non}
[BRANCH_TRACKER] DÉCISION: {SUPPRIMER|PROTÉGER|CLARIFIER}
[BRANCH_TRACKER] Raison: {raison}
```

### Règles de décision

```
Si PR merged + branche non supprimée:
  → SUPPRIMER (nettoyage post-merge)

Si âge > 30j + PR aucune + intent non vivant:
  → SUPPRIMER (branche abandonnée)

Si âge > 30j + intent vivant (issue/epic ouverte):
  → PROTÉGER + ajouter commentaire sur issue liée

Si nom sans préfixe connu:
  → CLARIFIER avant toute action

Si branche = main|master|develop|staging:
  → JAMAIS SUPPRIMER (branche protégée)
```

## Application session 2026-06-18 (ECOS-CLI)

Branches supprimées durant la session :

| Branche | Intent détecté | État | Décision |
|---|---|---|---|
| `feature/remove-llm-rules` | NOUVELLE_FONCTIONNALITÉ | Mergée (PR #34) | ✅ SUPPRIMER |
| `feature/audit-branch-cleanup` | NOUVELLE_FONCTIONNALITÉ | Mergée (PR #35) | ✅ SUPPRIMER |
| `refactor/restructure-docs` | REFACTORING | Abandonnée > 30j | ✅ SUPPRIMER |
| `feature/sync-improvements` | NOUVELLE_FONCTIONNALITÉ | Abandonnée > 30j | ✅ SUPPRIMER |
| `fix/token-expiry` | CORRECTION_BUG | Abandonnée > 30j | ✅ SUPPRIMER |

## Intégration écosystème

- **Avant** : `ctulu-tool-selector` (choisir `branch-cleaner` vs mcp_github natif)
- **Après** : `hook-validation-reporter` (rapport post-nettoyage)
- **Outil CTULU** : `branch-cleaner` pour le nettoyage batch
- **Outil GitHub** : `mcp_github delete_branch` pour suppressions ponctuelles
- **Règle** : ne jamais supprimer sans ce protocole sur les repos CRITICAL/HIGH
