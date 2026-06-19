---
type: skill
version: "1.0.1"
date: "2026-06-19"
intent_hash: 0xBRANCH_LIFECYCLE_INTENT_TRACKER_phi1.000
status: active
trit_primitive: TritTrackBranch
tags: [branch, lifecycle, intent, git-governance, orphan-detection]
layer: "L3_DEVTOOLS"
nexusTags: ["CONFORME_NEXUS", "BRANCH_GOVERNANCE", "INTENT_TRACKING"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 — gap lifecycle branches detecte (feat/marrpc-v3 4 mois orpheline)"}
  - {v: "1.0.1", date: "2026-06-19", notes: "Harmonisation intent_hash phi convention (phi vs φ unicode)"}
---

# branch-lifecycle-intent-tracker

## Purpose

Associe chaque branche git à son **EPIC d'origine**, sa **passe de création**, et une **date de péremption estimée**. Alerte si une branche dépasse N jours sans PR ouverte. Complément de `branch-audit-cleanup` pour la dimension intentionnelle — répond à la question "*pourquoi cette branche existe-t-elle ?*" avant de la supprimer.

## Trigger

Utiliser quand :
- création d'une nouvelle branche `feature/`, `fix/`, `adr-`, `refactor/`
- branche > 30 jours sans PR ouverte
- audit branches orphelines détecté
- validation BRGS pre-push
- question "peut-on supprimer cette branche ?"

## Modèle d'intent par branche

```yaml
branch:
  name: feature/t32-cas-gh-passe6
  repo: gerivdb/ECOS-CLI
  created: 2026-06-17
  created_by: ENV1 (Perplexity passe 6)
  epic_origin: T32 — CAS GitHub integration
  passe_origin: PASSE-6 LORE transposition
  expected_lifetime_days: 7
  pr_number: 962
  pr_status: merged
  verdict: SAFE_DELETE
```

## Classification des branches

| Type | Préfixe attendu | Lifetime max | Règle |
|---|---|---|---|
| Feature EPIC | `feature/` | 14 jours | PR obligatoire < 7 jours |
| Correctif | `fix/` | 7 jours | PR obligatoire < 3 jours |
| ADR | `adr-` | 30 jours | Review NEXUS requise |
| Refactor | `refactor/` | 21 jours | PR + validation strate |
| Feature non-std | Tout autre | 0 jours | WARN immédiat → vérifier |

## Protocole d'audit

### Pour chaque branche active

```
[BRANCH_TRACKER] Branche: {nom}
[BRANCH_TRACKER] Age: {N} jours
[BRANCH_TRACKER] PR associée: {numéro} | ORPHELINE
[BRANCH_TRACKER] Epic/Passe: {contexte} | INCONNU
[BRANCH_TRACKER] Verdict: ACTIVE | PÉRIMÉE | SAFE_DELETE | ORPHELINE_CRITIQUE
```

### Règles de verdict

```
PR mergée                   → SAFE_DELETE (supprimer immédiatement)
PR ouverte                  → ACTIVE (conserver)
Pas de PR + age < 7j        → RÉCENTE (surveiller)
Pas de PR + age 7-30j       → PÉRIMÉE (demander intention)
Pas de PR + age > 30j       → ORPHELINE_CRITIQUE (action requise)
Préfixe non-standard        → WARN + vérification manuelle
```

## Cas réel — session ECOS-CLI 2026-06-18

```
feat/marrpc-v3-consolidation
  Age: ~4 mois (créée 2026-02-22)
  PR: AUCUNE
  Verdict: ORPHELINE_CRITIQUE
  Action: supprimée après vérification du message commit
  ("validé en review" → travail déjà intégré ailleurs)
```

Ce skill aurait détecté cette branche à J+30 et généré une alerte préventive.

## Intégration écosystème

- **Complèmente** : `branch-audit-cleanup` (action de suppression)
- **Alimente** : `hook-validation-reporter` (rapport BRGS enrichi avec intent)
- **Référence** : `BRIDGES.yaml` (pre_decision_checks avant toute suppression)
- **Déclenche** : HITL si branche `adr-*` périmée (impact gouvernance L0)
