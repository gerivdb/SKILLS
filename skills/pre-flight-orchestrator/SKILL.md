---
type: GUI
version: "2.0.0"
date: "2026-06-08"
intent_hash: 0xPRE_FLIGHT_ORCHESTRATOR_V2_20260608
status: active
---

# Skill: pre-flight-orchestrator

## Purpose
Orchestrate mandatory pre-flight checks before any multi-repo session. Ensures all prerequisite validations are completed before work begins.

## Context
Multi-repo sessions systematically forget prerequisite checks (path, remote, branch, status, untracked, doc-format). This orchestrator chains the 8 existing skills in mandatory sequence. Steps updated to reflect merged skills (v2).

## Regle
Toute session impliquant 2+ repos ou un plan multi-phase DOIT executer le pre-flight avant toute action.

## Sequence obligatoire

1. `repo-path-resolver` - valider tous les chemins cibles (L0-L5 strata)
2. `ARGUS-REMOTE-AUDITOR` - valider tous les remotes
3. `branch-guard` - verifier la branche courante vs attendue
4. `workspace-audit` - verifier working tree propre + lister untracked (merged: workspace-sanitizer + untracked-auditor)
5. `doc-gate` - verifier les statuts PRD/EPIC/INTENT + lire regles hooks (merged: doc-status-validator + git-hook-enforcer)

[WARN] **Changes from v1:**
- Step 4: use `workspace-audit` (replaces `workspace-sanitizer` + `untracked-auditor`)
- Step 5: use `doc-gate` (replaces `doc-status-validator` + `git-hook-enforcer`)
- Old skills still work but are deprecated

## Rapport
Generer `.kilo/preflight/PREFLIGHT_REPORT.yaml` :
- `timestamp`
- `repo` + `branch`
- `checks` : liste des 6 checks avec `status: PASS|FAIL|WARN`
- `blockers` : liste des echecs bloquants
- `actions` : liste des actions autorisees post-pre-flight

## Regles de blocage
- Si `workspace-sanitizer` detecte > 10 fichiers modifies non lies -> STOP
- Si `branch-guard` detecte mismatch sur branche feature -> STOP
- Si `repo-path-resolver` trouve un chemin manquant -> STOP
- Si `doc-status-validator` trouve un statut invalide -> STOP

## Anti-pattern interdit
- Executer le plan sans pre-flight
- Ignorer un FAIL et continuer
- Generer un rapport sans executer les 6 checks

## Exemple d'application
```
Session : implementation metacluster PR (3 repos)
-> Pre-flight execute sur KIVA-CLI, diff0-fork, NEXUS
-> Checks : PASS / PASS / PASS / PASS / WARN / PASS
-> WARN : 2 untracked dans KIVA-CLI (review.py, tql.py)
-> Action : demander instruction avant creation fichier dans cli/commands/
-> Plan autorise sur diff0-fork et NEXUS uniquement
```
