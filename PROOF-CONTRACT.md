# PROOF-CONTRACT — Contrat de preuve GERIVDB
Version: v2.18.0.0
Strate: ENV2.env / ENV3.pur / ENV6.mesh

## Préambule
Tout mandat ouvert dans le métacluster GERIVDB se conforme aux 14 principes ci-dessous.
Un livrable qui ne s'y conforme pas est REFUSÉ, pas débattu.

---

## Les 14 principes (référence courte)

| # | Principe | Règle courte |
|---|----------|--------------|
| P1 | Zéro Fausse Fin | Aucun succès sans artefact |
| P2 | Trois niveaux de preuve | PROUVÉ > ATTESTÉ > DÉCRIT ; seul PROUVÉ vaut clôture |
| P3 | Fait vs interprétation | Pas d'adverbe sur-affirmatif ("parfaitement", "irréfutable") |
| P4 | Recoupement | 2 artefacts indépendants minimum |
| P5 | Cohérence nom/contenu | timestamp_utc == filename_timestamp |
| P6 | Sémantique scellée | 1 champ = 1 sens, figé par REF |
| P7 | Périmètre verrouillé | Pas de scope creep silencieux |
| P8 | Anti-pattern PRD-113 | Le writer d'un WAL est le système, pas un script ad hoc |
| P9 | WAL de clôture fourni | « décrit » ≠ « fourni » |
| P10 | Ordre consignations | REF avant commit ; rectification avant clôture |
| P11 | Cohérence inter-shards | Contradiction consignée avant action |
| P12 | Traçabilité PID | pid + pid_role dans chaque WAL et log |
| P13 | Décisions binaires | Q1(a/b/c), Q2(a/b), Q3(a/b) — pas de question ouverte |
| P14 | Séquence imposée | Plan validé HITL, non modifiable sans REF |

---

## Checklist avant clôture (à produire systématiquement)

- [ ] WAL de clôture au format JSON brut, fourni (pas décrit)
- [ ] Chaque critère d'acceptation : PROUVÉ / ATTESTÉ / DÉCRIT / ABSENT, avec artefact
- [ ] WAL failure (si applicable) : nom/timestamp concordants, `action: DOM_BRIDGE_FAILURE`, `scope: task-E-failure-proof`
- [ ] Log serveur recoupé avec WAL (P4)
- [ ] `git log` + `git show` pour tout commit revendiqué
- [ ] Aucun fichier hors périmètre dans le WAL (P7)
- [ ] PID présent avec `pid_role` (P12)
- [ ] REF de rectification consignée si erreur factuelle détectée (P10, P11)

## Citoyens de référence

| Citoyen | Rôle | Statut |
|---------|------|--------|
| `SKILL-REGISTRY` | Gouvernance des skills : registre, validation, intégration, WAL | À exercer |
| `WORKTREE-GUARDIAN` | Gouvernance des worktrees : orphelins, strate L*, nettoyage | À exercer |
| `AUDIT-GUARDIAN` | Vérifie P1/P2/P3/P4/P8/P9/P10 | À créer |
| `CONSISTENCY-GUARDIAN` | Vérifie P11 | À créer |
| `WAL-GUARDIAN` | Vérifie P5/P6/P12 | À créer |
| `SCOPE-GUARDIAN` | Vérifie P7/P14 | À créer |

## Méta-skills de référence

| Méta-skill | Rôle |
|------------|------|
| `skill-proof-validator` | Vérifie qu'une claim est accompagnée d'artefacts bruts (P2) |
| `skill-wal-auditor` | Audite chaque fichier WAL (P5/P6/P12) |
| `skill-scope-guard` | Vérifie qu'un livrable respecte le périmètre écrit (P7) |
| `skill-rectification-writer` | Écrit un REF de rectification (P10/P11) |
| `skill-closure-auditor` | Vérifie qu'un mandat est clos selon tous ses critères (P9) |
| `skill-sequence-enforcer` | Vérifie qu'une séquence est respectée dans l'ordre (P14) |

## Règle d'ouverture de mandat

Aucun mandat n'est ouvert sans :
1. Périmètre écrit, critères d'acceptation numérotés, artefacts attendus
2. Séquence proposée et validée HITL
3. Référence explicite aux 14 principes applicables
4. Mention des citoyens invoqués

## Règle de clôture de mandat

Aucun mandat n'est clos sans :
1. WAL de clôture JSON brut fourni (pas décrit)
2. Checklist P3 remplie (critère par critère)
3. REF de rectification si erreur factuelle détectée
4. Décompte final (tests, artefacts, gaps) aligné sur le périmètre écrit

---

*Document généré automatiquement · gerivdb/SKILLS · v2.18.0.0*