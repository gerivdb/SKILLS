# Skill: pre-flight-orchestrator

## Contexte
Une session multi-repo oublie systématiquement des checks préalables (path, remote, branch, status, untracked, workspace, doc-format). Ces oublis reproduisent les lacunes corrigées par les 8 skills existants.

## Règle
Toute session impliquant 2+ repos ou un plan multi-phase DOIT exécuter le pre-flight avant toute action.

## Séquence obligatoire
1. `repo-path-resolver` — valider tous les chemins cibles
2. `ARGUS-REMOTE-AUDITOR` — valider tous les remotes
3. `branch-guard` — vérifier la branche courante vs attendue
4. `workspace-sanitizer` — vérifier working tree propre
5. `untracked-auditor` — lister et classer les untracked
6. `doc-status-validator` — vérifier les statuts PRD/EPIC/INTENT

## Rapport
Générer `.kilo/preflight/PREFLIGHT_REPORT.yaml` :
- `timestamp`
- `repo` + `branch`
- `checks` : liste des 6 checks avec `status: PASS|FAIL|WARN`
- `blockers` : liste des échecs bloquants
- `actions` : liste des actions autorisées post-pre-flight

## Règles de blocage
- Si `workspace-sanitizer` détecte > 10 fichiers modifiés non liés → STOP
- Si `branch-guard` détecte mismatch sur branche feature → STOP
- Si `repo-path-resolver` trouve un chemin manquant → STOP
- Si `doc-status-validator` trouve un statut invalide → STOP

## Anti-pattern interdit
- Exécuter le plan sans pre-flight
- Ignorer un FAIL et continuer
- Générer un rapport sans exécuter les 6 checks

## Exemple d'application
```
Session : implémentation métacluster PR (3 repos)
→ Pre-flight exécuté sur KIVA-CLI, diff0-fork, NEXUS
→ Checks : PASS / PASS / PASS / PASS / WARN / PASS
→ WARN : 2 untracked dans KIVA-CLI (review.py, tql.py)
→ Action : demander instruction avant création fichier dans cli/commands/
→ Plan autorisé sur diff0-fork et NEXUS uniquement
```
