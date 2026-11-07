---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-12"
intent_hash: 0xSKILL_SESSION_START_CHECKLIST_20260812
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/session-start-checklist/SKILL.md
---

# Skill — session-start-checklist

Checklist obligatoire de démarrage de session pour garantir que la doctrine
CI, les règles ADR et l'état sanitaire du repo sont vérifiés avant toute
modification.

## Objectifs
- Bloquer les implémentations GitHub Actions non autorisées.
- Purger les processus zombies avant toute session.
- Vérifier la doctrine CI locale KIVA-CLI.
- Audit rapide des règles Kilo pertinentes.
- Rapport de démarrage traçable.

## Déclencheur
- Début de toute session KiloCode sur GeriCode.
- Avant toute modification de CI, workflow, ou gouvernance.
- Après une période d'inactivité > 4h.

## Entrées
- `repo_path`: chemin du repo cible.
- `strict`: booléen, bloquant si True.

## Sorties
- `ok`: booléen, True si tous les checks passent.
- `report`: dict, détail des checks.

## Checks obligatoires

### CHECK-1 — Blocage GitHub Actions
- Vérifier l'absence de `.github/workflows/` dans le repo.
- Si présent → bloquer et rappeler ADR-024.
- Réf: `docs/KIVACLI-GIT-ZOMBIE-HOOKS.md`, `.kilo/workflows/README.md`

### CHECK-2 — Hygiène processus
- Détecter les processus zombies (git, node, python, zig, cargo, bun, pwsh, trixd, kix, electron, Code).
- Critères: StartTime > 2h, CPU = 0.
- Si zombies > 0 → avertir et proposer purge.
- Réf: citizen `process-zombie-hygiene`, design `zombie-symptom`

### CHECK-3 — Doctrine CI locale
- Vérifier la présence de `.kiva/ci.yaml`.
- Vérifier la présence de `.kilo/workflows/`.
- Si absent → signaler et proposer génération via `kiva-ci-local`.
- Réf: skill `kiva-ci-local`

### CHECK-4 — Audit règles ADR
- Vérifier la cohérence des règles Kilo avec les ADRs backing.
- Vérifier l'absence de contradictions avec ADR-024.
- Réf: skill `kilo-rule-auditor`

### CHECK-5 — Audit repo
- Vérifier la SOT `known_repositories.yaml`.
- Vérifier `agent-manager.json` et worktrees.
- Réf: skill `audit-repo`, skill `kilo-worktree-reconciler`

## Rapport

Format JSON:
```json
{
  "timestamp": "ISO8601",
  "repo": "...",
  "checks": {
    "github_actions_blocked": true,
    "process_hygiene_ok": true,
    "kiva_cli_doctrine_ok": true,
    "adr_rules_ok": true,
    "repo_audit_ok": true
  },
  "zombies_detected": 0,
  "blocked": false,
  "actions": []
}
```

## Intégration
- Peut être invoqué en standalone: `pwsh -File .kiva/scripts/session-start-checklist.ps1`
- Peut être appelé par `session-boot-sequence` (BOOT-0, BOOT-1).
- Peut être déclenché par le citizen `rule-sanitizer` en pré-session.

## Anti-patterns
- Démarrer une session sans exécuter ce checklist.
- Ignorer un check en échec et poursuivre.
- Modifier `.github/workflows/` sans passer par KIVA-CLI.

## Référence ADR
- **ADR** : ADR-024 (CI souveraine KIVA-CLI)
- **ADR** : ADR-2026-08-09-001-GIT_HYGIENE_MECHANISMS
- **IntentHash** : `0xSKILL_SESSION_START_CHECKLIST_20260812`
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
