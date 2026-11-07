---
name: friction-analysis
description: Analyse TALEX des frictions/erreurs ERR survenues durant une session. Utiliser pour détecter les patterns d'erreur récurrents et générer des corrections structurelles. Exécute talex_friction_analyzer.py + talex_structural_fixes_applier.py.
version: 1.0.0
intent_hash: 0xFRICTION_ANALYSIS_20260920
---

# Friction Analysis

## Objectif
Détecter, classifier et corriger les frictions/erreurs ERR survenues durant une session KiloCode.

## Déclencheur
- Fin de session complexe multi-repo
- Erreurs PowerShell, SQLite, imports, chemins
- Besoin d'analyse causale des erreurs

## Protocole

### Tâche A — Analyser les frictions (P0)

**Fichier** : `scripts/talex_friction_analyzer.py` (existant)
**Action** : exécuter l'analyseur de frictions
**Critères** :
- [ ] Rapport JSON généré dans `reports/talex_friction_analysis_<date>.json`
- [ ] Issues classées par sévérité (critical/high/medium/low)
- [ ] Structural fixes identifiées

### Tâche B — Appliquer les corrections (P0)

**Fichier** : `scripts/talex_structural_fixes_applier.py` (existant)
**Action** : appliquer les corrections structurelles
**Critères** :
- [ ] Mode dry-run d'abord : `python scripts/talex_structural_fixes_applier.py`
- [ ] Mode apply : `python scripts/talex_structural_fixes_applier.py --apply`
- [ ] Chaque fix vérifié individuellement

### Tâche C — Valider (P0)

**Action** : vérifier que les corrections n'ont pas cassé les tests
**Critères** :
- [ ] Tests existants passent
- [ ] Pas de régression

## Critères de succès
- [ ] Rapport friction généré
- [ ] Corrections appliquées
- [ ] Tests passent

## Coordination
| Repo | Action |
|---|---|
| **HERMES** | Exécuter l'analyseur |

## Références
- `scripts/talex_friction_analyzer.py` — Analyseur de frictions
- `scripts/talex_structural_fixes_applier.py` — Applicateur de corrections
- `reports/talex_friction_analysis_*.json` — Rapports générés

---

## Proof-of-Life
- [x] 2026-09-20T21:55:00+02:00 — Skill créé : friction-analysis
